
import re

def _regex_tokenizer_builder(regex, token_type):
    def tokenizer(tokens):
        for type, s in tokens:
            if type != '?':
                yield (type, s)
                continue

            match = regex.search(s)

            if match:
                while match:
                    g = match.groups()
                    yield ('?', g[0])
                    yield (token_type, g[1])
                    match = regex.search(g[2])

                yield ('?', g[2])
            else:
                yield ('?', s)

    return tokenizer

_string_tokenizer = _regex_tokenizer_builder(
    re.compile(r'^(.*?)(".*?(?<!\\)")(.*)$'),
    'STRING'
)

_identifier_tokenizer = _regex_tokenizer_builder(
    re.compile(r'^(.*?)([A-Za-z_][A-Za-z0-9_]*)(.*)$'),
    'ID'
)

_number_tokenizer = _regex_tokenizer_builder(
    re.compile(r'^(.*?)([0-9]+)(.*)$'),
    'NUMBER'
)

_whitespace_tokenizer = _regex_tokenizer_builder(
    re.compile(r'^(.*?)([ \t\r\f\v]+)(.*)$'),
    'WS'
)

def _keyword_tokenizer(tokens):
    for type, token in tokens:
        if type == 'ID':
            if token == 'def':
                yield ('DEF', token)
            elif token == 'expression':
                yield ('EXPRESSION', token) #TODO: remove me
            elif token == 'call':
                yield ('CALL', token) #TODO: remove me
            else:
                yield (type, token)
        else:
            yield (type, token)

def _comment_tokenizer(tokens):
    comment = ''
    for type, token in tokens:
        if comment:
            comment += token
            continue

        if type != '?':
            yield (type, token)
            continue

        elif '#' in token:
            loc = token.find('#')
            yield ('?', token[:loc])
            comment = token[loc:]
        else:
            yield ('?', token)

    if comment:
        yield ('COMMENT', comment)

def _operator_tokenizer(tokens):
    for type, token in tokens:
        if type != '?':
            yield (type, token)
            continue

        for s in token:
            if s == '{':
                yield ('L_CURLY', s)
            elif s == '}':
                yield ('R_CURLY', s)
            elif s == '(':
                yield ('L_PAREN', s)
            elif s == ')':
                yield ('R_PAREN', s)
            elif s == '[':
                yield ('L_SQUARE', s)
            elif s == ']':
                yield ('R_SQUARE', s)
            elif s == '=':
                yield ('EQUAL', s)
            elif s == ',':
                yield ('COMMA', s)
            elif s == '*':
                yield ('STAR', s)
            elif s == '+':
                yield ('PLUS', s)
            elif s == '-':
                yield ('MINUS', s)
            elif s == '/':
                yield ('SLASH', s)
            else:
                yield('?', s)

def _nulls_filter_tokenizer(tokens):
    for type, s in tokens:
        if s != '':
            yield (type, s)

def _tag_tokens_with_position(tokens):
    position = 1
    for type, token in tokens:
        yield (type, token, position)
        position += len(token)

def tokenize(line):
    tokens = [('?', line), ('NL', '\n')]

    tokens = _string_tokenizer(tokens)
    tokens = _comment_tokenizer(tokens)
    tokens = _identifier_tokenizer(tokens)
    tokens = _number_tokenizer(tokens)
    tokens = _keyword_tokenizer(tokens)
    tokens = _whitespace_tokenizer(tokens)

    tokens = _operator_tokenizer(tokens)

    tokens = _nulls_filter_tokenizer(tokens)
    tokens = _tag_tokens_with_position(tokens)
    tokens = list(tokens)

    return tokens
