
import json
from runtime.interpreter.expressions import *

class ExecutionError(ValueError):
    pass



class PrintFunction(Value):
    def call(self, parameters, symbol_table):
        for param in parameters:
            if isinstance(param, String):
                print(param.value, end='')
        print('')


# Statements

class DeclarationStatement(ASTObject):
    def __init__(self, obj):
        self.name = obj['name']
        self.value = ast_creator(obj['value']).value()

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        print('value: ', self.value)

        return {
            **symbol_table,
            self.name: self.value
        }


class FunctionCallExpression(ASTObject):
    def __init__(self, obj):

        if isinstance(obj['function'], str):
            self.function = Id({
                'value': obj['function']
            })
        else:
            self.function = ast_creator(obj['function'])

        self.parameters = [ast_creator(x) for x in obj['parameters']]

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        if self.function.value in symbol_table:
            stack = {
                **symbol_table,
            }
            f = symbol_table[self.function.value]
            print('ISINSTANCE OF VALUE: ', isinstance(f, Value))
            f.call(self.parameters, stack) #TODO: we are sending in the symbol_table, this is like python where the values are based on what is defined alread. We don't want it like that, or do we?
            #TODO: handle return statment
        else:
            ValueError('function not found')
        return {**symbol_table}


# Top Level

class TopLevel(ASTObject):
    def __init__(self, obj):
        self.statements = [ast_creator(x) for x in obj['statements']]

    def visit(self, symbol_table):
        for statment in self.statements:
            symbol_table = statment.visit(symbol_table)

        if '__main__' not in symbol_table:
            raise ExecutionError('could not find __main__')

        main = FunctionCallExpression({
            'function': '__main__',
            'parameters': []
        })
        symbol_table = main.visit(symbol_table)

        return {**symbol_table}


def ast_creator(obj):
    def find_class(type):
        if type == 'declaration_statement': #TODO: find using reflections
            return DeclarationStatement
        elif type == 'function_call_expression':
            return FunctionCallExpression
        elif type == 'lambda_expression':
            return lambda obj: LambdaExpression(obj, lambda statments: [ast_creator(x) for x in statments])
        elif type == 'string':
            return String
        elif type == 'id':
            return Id
        else:
            raise ValueError('type not available `{}`'.format(type))
            return None
    clazz = find_class(obj['type'])
    return clazz and clazz(obj)


def interpret(ast):

    version = ast['version']
    start = ast['statements']

    if version != '0.0.1':
        raise ExecutionError('File requires version "0.0.1"')

    top_level = TopLevel(ast)
    global_symbols = {
        'print': PrintFunction(),
    }

    top_level.visit(global_symbols)

    return 0