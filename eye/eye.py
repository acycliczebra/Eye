
import compiler
import json
from runtime import interpreter

test = '''def __main__ [args]{
    print("2 + 2 / 2")
    print(2 + 2 / 2)
}
'''

ast = compiler.compile(test)

print(json.dumps(ast, indent=2))

ret_code = interpreter.interpret(ast)

print(ret_code)