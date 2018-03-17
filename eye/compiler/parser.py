import logging
import json

class ParserError(Exception):
    pass


class Tokens:
    NONE = 'NONE'
    IGNORE = 'IGNORE'

class TokenBuffer:
    def __init__(self, tokens):
        self.tokens = tokens[:]
        self.pointer = 0

    #TODO: add increment, decrement and access, and to_bool

def any_of(*accepts):
    def f(tokens):

        for accept in accepts:
            tokens, result = accept(tokens)
            if result not in [Tokens.NONE, Tokens.IGNORE]:
                return tokens, result

        return tokens, Tokens.NONE

    return f

def all_of(*accepts):
    def f(tokens):
        orig = tokens[:]
        results = []
        for accept in accepts:
            tokens, result = accept(tokens)
            if result == Tokens.NONE:
                return orig, Tokens.NONE
            elif result == Tokens.IGNORE:
                continue
            else:
                results += [result]

        return tokens, results

    return f

def many_of(accept):
    def f(tokens):
        results = []
        while tokens:
            tokens, result = accept(tokens)
            if result == Tokens.NONE:
                break
            elif result == Tokens.IGNORE:
                continue
            else:
                results += [result]
        return tokens, results
    return f

def maybe(accept):
    def f(tokens):
        tokens, result = accept(tokens)
        if result == Tokens.NONE:
            result = Tokens.IGNORE
        return tokens, result
    return f

def supress(accept):
    def f(tokens):
        tokens, result = accept(tokens)
        if result != Tokens.NONE:
            result = Tokens.IGNORE
        return tokens, result
    return f

def ignore(accept):
    def f(tokens):
        tokens, result = accept(tokens)
        return tokens, Tokens.IGNORE
    return f

def no_leading_nl(accept):
    def f(tokens):
        _, token = get_first_token(tokens, ignore=['WS', 'COMMENT'])
        if token == 'NL':
            return tokens, Tokens.IGNORE
        tokens, result = accept(tokens)
        return tokens, result
    return f

def interlace(accept, delimeter):
    def f(tokens):

        results = []
        tokens, result = accept(tokens)
        if result == Tokens.NONE:
            return tokens, Tokens.NONE
        elif result == Tokens.IGNORE:
            pass
        else:
            results += [result]

        while True:
            tokens, result = all_of(delimeter, accept)(tokens)
            if result == Tokens.NONE:
                break

            results += [result[-1]]

        return tokens, results
    return f


#TODO: I don't think these are right
supress_many_or_zero = lambda accept: supress(many_of(accept))
ignore_many = lambda accept: ignore(many_of(accept))
supress_many = lambda accept: all_of(supress(accept), supress_many(accept))


def get_first_token(tokens, ignore=None):
    if ignore == None:
        ignore = ['WS', 'NL', 'COMMENT']

    i = 0
    try:
        while tokens[i]['type'] in ignore:
            i += 1
    except IndexError:
        return tokens, None

    return tokens[i+1:], tokens[i]


def accept_token(types, ignore=None):
    if ignore == None:
        ignore = ['WS', 'NL', 'COMMENT']

    def f(tokens):
        next_tokens, next_token = get_first_token(tokens, ignore)

        if isinstance(types, str):
            my_types = [types]
        elif isinstance(types, list):
            my_types = types

        if next_token is None:
            return tokens, Tokens.NONE

        if next_token['type'] in my_types:
            return next_tokens, {
                'type': next_token['type'].lower(),
                'value': next_token['text'],
            }

        return tokens, Tokens.NONE
    return f

def debug_accept(accept):
    def f(tokens):
        logging.debug('accepting: %s -> %s', accept.__name__, tokens[0] if tokens else 'EOF')
        tokens, result = accept(tokens)
        if result == Tokens.NONE:
            logging.debug('failed: %s', accept.__name__)
        elif result == Tokens.IGNORE:
            logging.debug('ignored: %s', accept.__name__)
        else:
            logging.debug('accepted: %s -> %s', accept.__name__, result)

        return tokens, result

    return f

@debug_accept
def accept_def(tokens): return accept_token('DEF')(tokens)
@debug_accept
def accept_id(tokens): return accept_token('ID')(tokens)
@debug_accept
def accept_ws(tokens): return accept_token('WS')(tokens)
@debug_accept
def accept_nl(tokens): return accept_token('NL')(tokens)
@debug_accept
def accept_comma(tokens): return accept_token('COMMA')(tokens)

@debug_accept
def accept_left_curly(tokens): return accept_token('L_CURLY')(tokens)
@debug_accept
def accept_right_curly(tokens): return accept_token('R_CURLY')(tokens)
@debug_accept
def accept_left_square(tokens): return accept_token('L_SQUARE')(tokens)
@debug_accept
def accept_right_square(tokens): return accept_token('R_SQUARE')(tokens)
@debug_accept
def accept_left_paren(tokens): return accept_token('L_PAREN')(tokens)
@debug_accept
def accept_right_paren(tokens): return accept_token('R_PAREN')(tokens)

@debug_accept
def accept_string_literal(tokens): return accept_token('STRING')(tokens)

@debug_accept
def accept_statement_list(tokens):

    tokens, statements = interlace(
        accept_statement,
        many_of(accept_nl)
    )(tokens)

    return tokens, statements

@debug_accept
def accept_function_args(tokens):

    tokens, result = all_of(
        supress(accept_left_square),
        interlace( #TODO: maybe id
            accept_id,
            accept_comma
        ),
        supress(accept_right_square),
    )(tokens)

    if result == Tokens.NONE:
        return tokens, Tokens.NONE

    [ids] = result
    ids = [x['value'] for x in ids]

    return tokens, ids

@debug_accept
def accept_lambda_expression(tokens):
    tokens, result = all_of(
        accept_function_args,
        supress(accept_left_curly),
        accept_statement_list, #TODO: maybe statement_list
        supress(accept_right_curly),
    )(tokens)

    if result == Tokens.NONE:
        return tokens, Tokens.NONE

    [args, statements] = result

    return tokens, {
        'type': 'lambda_expression',
        'args': args,
        'statements': statements,
    }

@debug_accept
def accept_expression(tokens):

    tokens, expression = any_of(
        accept_lambda_expression,
        accept_id,
        accept_string_literal,
    )(tokens)

    return tokens, expression

@debug_accept
def accept_function_call_statement(tokens):

    tokens, result = all_of(
        accept_expression,
        supress(accept_left_paren),
        interlace(
            accept_expression,
            accept_comma
        ),
        supress(accept_right_paren),
    )(tokens)

    if result == Tokens.NONE:
        return tokens, Tokens.NONE

    [function, parameters] = result

    return tokens, {
        'type': 'function_call_statement',
        'function': function,
        'parameters': parameters,
    }

@debug_accept
def accept_declaration_statement(tokens):

    tokens, result = all_of(
        accept_def,
        no_leading_nl(accept_id),
        no_leading_nl(accept_expression),
    )(tokens)

    if result == Tokens.NONE:
        return tokens, Tokens.NONE

    [_, id, value] = result

    return tokens, {
        'type': 'declaration_statement',
        'name': id['value'],
        'value': value,
    }


@debug_accept
def accept_statement(tokens):

    tokens, statement = any_of(
        accept_declaration_statement,
        accept_function_call_statement
    )(tokens)

    return tokens, statement

@debug_accept
def accept_top_level(tokens):

    tokens, statements = accept_statement_list(tokens)

    return tokens, statements

def parse(tokens):

    tokens, statements = accept_top_level(tokens)

    result = {
        "version": "0.0.1",
        "statements": statements
    }

    return result
