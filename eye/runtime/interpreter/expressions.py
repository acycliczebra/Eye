
class Value:
    def show(self):
        pass
    def call(self, parameters, symbol_table):
        raise NotImplemented('object not callable')
    def __add__(self, parameters, symbol_table):
        raise NotImplemented('object not addable')

class FunctionValue(Value):
    def __init__(self, args, statements):
        self.args = args
        self.statements = statements
    def call(self, parameters, symbol_table):
        #TODO: check if arg and parameters have the same length
        stack = {**symbol_table}
        for arg, param in zip(self.args, parameters):
            stack[arg] = param

        for statement in self.statements:
            stack = statement.visit(stack)

class NumberValue(Value):
    def __init__(self, value):
        self.value = float(value)
    def __add__(self, other):
        return self.value + other.value

class StringValue(Value):
    def __init__(self, value):
        self.value = value
    def call(self, parameters, symbol_table):
        raise ValueError('object not callable')


class ASTObject:
    def visit(self, symbol_table):
        return {**symbol_table}


class Expression(ASTObject):
    def value(self, symbol_table):
        raise NotImplementedError('abstract method `' + str(type(self)) + '`')

class LambdaExpression(Expression):
    def __init__(self, obj, statment_cb):
        self.args = obj['args']
        self.statements = statment_cb(obj['statements'])

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        return {**symbol_table}

    def value(self, symbol_table):

        return FunctionValue(self.args, self.statements)

class String(Expression):
    def __init__(self, obj):
        self._value = obj['value']

    def visit(self, symbol_table):
        return {**symbol_table}

    def value(self, symbol_table):
        return StringValue(self._value)

class Number(Expression):
    def __init__(self, obj):
        self._value = obj['value']

    def visit(self, symbol_table):
        return {**symbol_table}

    def value(self, symbol_table):
        return NumberValue(self._value)


