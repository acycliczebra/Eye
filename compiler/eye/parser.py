
import json

class ParserError(Exception):
    pass

class Syntax:
    pass

class Tokens:
    NONE = 'NONE'
    IGNORE = 'IGNORE'


def _bracket_parser(tokens):
    def helper(tokens, stack, i):
        res = []
        while i < len(tokens):
            token = tokens[i]
            type = token['type']
            if 'L_' in type:
                stack += [type]
                new_tokens, stack, i = helper(tokens, stack, i+1)

                res += [[token] + new_tokens]
            elif 'R_' in type:
                corresponding = type.replace('R_', 'L_')
                if not stack or stack[-1] != corresponding:
                    raise ParserError('mismatched brackets')
                stack = stack[:-1]

                res += [token]
                return res, stack, i
            else:
                res += [token]
            i += 1
        return res, stack, i

    expected_i = len(tokens)
    tokens, stack, i = helper(tokens, [], 0)

    if stack:
        raise ParserError('mismatched brackets')
    if i != expected_i:
        raise ParserError('mismatched brackets')

    return tokens


def _parse(tokens):
    def print_tokens(tokens, depth=0):
        for token in tokens:
            if isinstance(token, list):
                print_tokens(token, depth=depth+1)
            else:
                print('\t' * depth, token)

    tokens = _bracket_parser(tokens)

    print_tokens(tokens)

    return []

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

#TODO: I don't think these are right
supress_many_or_zero = lambda accept: supress(many_of(accept))
ignore_many = lambda accept: ignore(many_of(accept))
supress_many = lambda accept: all_of(supress(accept), supress_many(accept))

def accept_token(token_type):
    def f(tokens):
        if not tokens:
            return tokens, Tokens.NONE

        if tokens[0]['type'] == token_type:
            return tokens[1:], {
                'type': token_type.lower(),
                'value': tokens[0]['text'],
            }

        return tokens, Tokens.NONE
    return f

accept_def = accept_token('DEF')
accept_id = accept_token('ID')
accept_ws = accept_token('WS')
accept_nl = accept_token('NL')
accept_comma = accept_token('COMMA')

accept_left_curly = accept_token('L_CURLY')
accept_right_curly = accept_token('R_CURLY')
accept_left_square = accept_token('L_SQUARE')
accept_right_square = accept_token('R_SQUARE')


def accept_statement_list(tokens):

    tokens, statements = many_of(
        all_of(
            accept_statement,
            supress(accept_nl), #sandwitch nl in statments
        )
    )(tokens)

    return tokens, statements

def accept_function_args(tokens):

    tokens, ids = all_of(
        supress(accept_left_square),
        accept_id, #TODO: accept many
        supress(accept_right_square),
    )(tokens)

    ids = [x['value'] for x in ids]

    return tokens, ids

def accept_lambda_expression(tokens):
    tokens, [args, statements] = all_of(
        accept_function_args,
        supress(accept_left_curly),
        ignore_many(accept_nl),
        accept_statement_list,
        ignore_many(accept_nl),
        supress(accept_right_curly),
    )(tokens)

    return tokens, {
        'type': 'lambda_expression',
        'args': args,
        'statements': statements,
    }

def accept_expression(tokens):

    tokens, expression = any_of(
        accept_lambda_expression
    )(tokens)

    return tokens, expression

# accept_expression = accept_token('EXPRESSION')
accept_function_call_statement = accept_token('CALL')

def accept_declaration_statement(tokens):

    tokens, result = all_of(
        accept_def,
        accept_id,
        accept_expression,
    )(tokens)

    if result == Tokens.NONE:
        return tokens, Tokens.NONE

    [_, id, value] = result

    return tokens, {
        'type': 'declaration_statement',
        'name': id['value'],
        'value': value,
    }


def accept_statement(tokens):

    tokens, statement = any_of(
        accept_declaration_statement,
        accept_function_call_statement
    )(tokens)

    return tokens, statement

def accept_top_level(tokens):
    tokens, statements = many_of(
        all_of(
            accept_statement,
            supress(accept_nl),
        )
    )(tokens)

    statements = [x[0] for x in statements]

    return tokens, statements

def parse(tokens):

    # remove whitespace
    tokens = [token for token in tokens if token['type'] != 'WS']
    tokens = [token for token in tokens if token['type'] != 'COMMENT']

    tokens, statements = accept_top_level(tokens)

    result = {
        "version": "0.0.1",
        "statments": statements
    }

    print('RESULT')
    print(json.dumps(result, indent=2))

    return statements, tokens
