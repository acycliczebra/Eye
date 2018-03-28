
import compiler
import json

test = '''def __main__ [args]{
    str = "2 + 2 / 2"
    print(str)
    print( 2 + 2 / 2)
}
'''

ast = compiler.compile(test)

print(json.dumps(ast, indent=2))

ret_code = compiler.run(test)

print(ret_code)