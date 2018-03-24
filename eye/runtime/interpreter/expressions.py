
class Value:
    def show(self):
        pass
    def call(self, parameters, symbol_table):
        pass


class ASTObject:
    def visit(self, symbol_table):
        print('FUNCTION: ', type(self).__name__)
        return {**symbol_table}


class Expression(ASTObject):
    def value(self):
        raise NotImplementedError('abstract method')

class LambdaExpression(Expression):
    def __init__(self, obj, statment_cb):
        self.args = obj['args']
        self.statements = statment_cb(obj['statements'])

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        return {**symbol_table}

    def value(self):
        class Function(Value):
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

        return Function(self.args, self.statements)

class Id(Expression):
    def __init__(self, obj):
        self.value = obj['value']

    def visit(self, symbol_table):
        return {**symbol_table}

class String(Expression):
    def __init__(self, obj):
        self.value = obj['value']

    def visit(self, symbol_table):
        return {**symbol_table}

class Number(Expression):
    def __init__(self, obj):
        self.value = obj['value']

    def visit(self, symbol_table):
        return {**symbol_table}


