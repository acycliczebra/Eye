
import json

class ExecutionError(ValueError):
    pass


class ASTObject:
    def visit(self, symbol_table):
        print('FUNCTION: ', type(self).__name__)
        return {**symbol_table}

# Statements

class DeclarationStatement(ASTObject):
    def __init__(self, obj):
        self.name = obj['name']
        self.value = ast_creator(obj['value'])

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

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

        if isinstance(self.function, Id): #TODO: better way of doing this, I'm not seeing the patter yet
            if self.function.value == 'print':
                for param in self.parameters:
                    if isinstance(param, String):
                        print(param.value, end='')
                print('')

            else:
                f = symbol_table[self.function.value]
                stack = {
                    **symbol_table,
                }
                #TODO: check if arg and parameters have the same length
                for arg, param in zip(f.args, self.parameters):
                    stack[arg] = param

                f.visit(stack) #TODO: we are sending in the symbol_table, this is like python. We don't want it like that, or do we?
                #TODO: handle return statment
        return {**symbol_table}

# Expressions

class LambdaExpression(ASTObject):
    def __init__(self, obj):
        self.args = obj['args']
        self.statements = [ast_creator(x) for x in obj['statements']]

    def visit(self, symbol_table):
        symbol_table = super().visit(symbol_table)

        for statment in self.statements:
            symbol_table = statment.visit(symbol_table)
        return {**symbol_table}

# Atoms

class Id(ASTObject):
    def __init__(self, obj):
        self.value = obj['value']

    def visit(self, symbol_table):
        return {**symbol_table}

class String(ASTObject):
    def __init__(self, obj):
        self.value = obj['value']

    def visit(self, symbol_table):
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
            return LambdaExpression
        elif type == 'id':
            return Id
        elif type == 'string':
            return String
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
    top_level.visit({})

    return 0