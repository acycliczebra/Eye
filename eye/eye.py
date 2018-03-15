
import compiler
from runtime import interpreter

test = r'''def __main__ [args]{
    print("Hello World")
}
'''

ast = compiler.compile(test)

ret_code = interpreter.interpret(ast)

print(ret_code)