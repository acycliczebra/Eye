
class Value:
    def show(self):
        raise NotImplemented('object not printable')
    def call(self, parameters, symbol_table):
        raise NotImplemented('object not callable')
    def __add__(self, other):
        raise NotImplemented('object not addable')
    def __sub__(self, other):
        raise NotImplemented('object not subtractable')
    def __mul__(self, other):
        raise NotImplemented('object not multipliable')
    def __truediv__(self, other):
        raise NotImplemented('object not dividable')

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
    def show(self):
        return self.value
    def __add__(self, other):
        return NumberValue(self.value + other.value)
    def __sub__(self, other):
        return NumberValue(self.value - other.value)
    def __mul__(self, other):
        return NumberValue(self.value * other.value)
    def __truediv__(self, other):
        return NumberValue(self.value / other.value)

class StringValue(Value):
    def __init__(self, value):
        self.value = value
    def show(self):
        return self.value
    def call(self, parameters, symbol_table):
        raise ValueError('object not callable')



class PrintFunction(Value):
    def call(self, parameters, symbol_table):
        for param in parameters:
            print(param.show(), end='')
        print('')


class AddFunction(Value):
    def call(self, parameters, symbol_table):
        if len(parameters) != 2:
            raise ExecutionError('expected 2 parameters')

        return parameters[0] + parameters[1]


class SubtractFunction(Value):
    def call(self, parameters, symbol_table):
        if len(parameters) != 2:
            raise ExecutionError('expected 2 parameters')

        return parameters[0] - parameters[1]

class MultiplyFunction(Value):
    def call(self, parameters, symbol_table):
        if len(parameters) != 2:
            raise ExecutionError('expected 2 parameters')

        return parameters[0] * parameters[1]

class DivisionFunction(Value):
    def call(self, parameters, symbol_table):
        if len(parameters) != 2:
            raise ExecutionError('expected 2 parameters')

        return parameters[0] / parameters[1]



