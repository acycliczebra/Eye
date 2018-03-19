
import compiler
import json
from runtime import interpreter

test = r'''def __main__ [args]{
    print("Hello World")
}
'''

ast = compiler.compile(test)

print(json.dumps(ast, indent=2))

ret_code = interpreter.interpret(ast)

print(ret_code)