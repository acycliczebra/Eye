

import runtime


script1 = '''

def main(arg): #TODO: main should be __main__
    print('hello world')
    return 6

'''

trigger1 = "cron */5 * * * *"

execute1 = {}


script2 = '''

def main(arg):
    a = arg['a'] * 7
    print('result is: ', a)
    return a

'''

trigger2 = "1 new result from script1"

execute2 = {
    "a": "take 1 from script1"
}


current_runtime = runtime.RuntimeEngine(language='.py')

current_runtime.load("script1", script1, trigger1, execute1)
current_runtime.load("script2", script2, trigger2, execute2)


current_runtime.execute()