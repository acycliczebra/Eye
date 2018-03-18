
import json

from . import tokenizer
from . import parser

class LexerError(Exception):
    pass


class Token:
    pass

class Line:

    def __init__(self, l):
        self.l = l
        self.tokens = tokenizer.tokenize(self.l)

    def is_empty(self):
        return self.l is None or self.l == ''

    def __str__(self):
        return '[#{} : `{}`]'.format(self.lineno, self.l) + '\n' + str(self.tokens)

class Program:
    def __init__(self, s):
        lines = [(i, Line(l)) for i, l in enumerate(s.split('\n'), 1)]
        #lines = [(i, l) for i, l in lines if not l.is_empty()]

        self.lines = lines

    def tokens(self):
        res = []
        lines = [(lineno, line.tokens) for lineno, line in self.lines]
        count = 0
        for lineno, line in lines:
            for type, s, pos in line:
                token = {
                    'type': type,
                    'text': s,
                    'position': {
                        'lineno': lineno,
                        'position': pos,
                    },
                    'id': count,
                }
                count += 1
                res += [token]
        return res

def lexer(s):
    return Program(s).tokens()



def parse(tokens):
    ast = parser.parse(tokens)
    return ast


def compile(s):
    tokens = lexer(s)
    ast = parse(tokens)
    #return json.dumps(ast, indent=2)
    return ast
