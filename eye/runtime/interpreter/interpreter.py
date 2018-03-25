
import json
from runtime.interpreter.values import *

class ExecutionError(ValueError):
    pass


class ASTObject:
    def visit(self, symbol_table):
        return {**symbol_table}


class Expression(ASTObject):
    def value(self, symbol_table):
        raise NotImplementedError('abstract method `' + str(type(self)) + '`')


    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        val = self.value(symbol_table)

        return {**symbol_table}

class LambdaExpression(Expression):
    def __init__(self, obj):
        self.args = obj['args']
        statement_cb = lambda statments: [ast_creator(x) for x in statments]
        self.statements = statement_cb(obj['statements'])

    def value(self, symbol_table):

        return FunctionValue(self.args, self.statements)

class String(Expression):
    def __init__(self, obj):
        self._value = obj['value']

    def value(self, symbol_table):
        return StringValue(self._value)

class Number(Expression):
    def __init__(self, obj):
        self._value = obj['value']

    def value(self, symbol_table):
        return NumberValue(self._value)

class FunctionCallExpression(Expression):
    def __init__(self, obj):
        self.function = ast_creator(obj['function'])
        self.parameters = [ast_creator(x) for x in obj['parameters']]

    def value(self, symbol_table):

        function = self.function.value(symbol_table)
        parameters = [x.value(symbol_table) for x in self.parameters]
        stack = {
            **symbol_table
        }
        result = function.call(parameters, stack) #TODO: we are sending in the symbol_table, this is like python where the values are based on what is defined alread. We don't want it like that, or do we?
        return result


class Id(Expression):
    def __init__(self, obj):
        self._value = obj['value']

    def visit(self, symbol_table):
        return {**symbol_table}

    def value(self, symbol_table):

        if self._value not in symbol_table:
            raise ValueError('result not found')
        result = symbol_table[self._value]
        return result


# Statements

class AssignmentStatement(ASTObject):
    def __init__(self, obj):
        if obj['to']['type'] != 'id':
            raise ValueError('only type of id supported for for lvalues')
        self.lvalue = obj['to']['value']
        self.rvalue = obj['value']

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        new_symbol_table = {**symbol_table}

        new_symbol_table[self.lvalue] = ast_creator(self.rvalue).value(symbol_table)
        return new_symbol_table

class DeclarationStatement(ASTObject):
    def __init__(self, obj):
        self.name = obj['name']
        self.raw_value = obj['value']

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        return {
            **symbol_table,
            self.name: ast_creator(self.raw_value).value(symbol_table)
        }


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
    def to_camel_case(snake_str):
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)

    def find_class(type):
        class_name = to_camel_case(type)
        if class_name in globals():
            return globals()[class_name]
        else:
            raise ValueError('type not available `{}`'.format(type))
            return None
    if isinstance(obj, str):
        return Id({
            'value': obj
        })
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
        '__add__': AddFunction(),
        '__sub__': SubtractFunction(),
        '__mul__': MultiplyFunction(),
        '__div__': DivisionFunction(),
    }

    top_level.visit(global_symbols)

    return 0