
import os
import sys

def shell(command):
    import subprocess as sp
    result = sp.run(command.split(' '), stdout=sp.PIPE)
    return result.stdout

def chdir():
    import os.path as p
    dir_path = p.dirname(p.realpath(__file__))
    dir_path = p.dirname(p.dirname(p.dirname(dir_path))) # Eye
    os.chdir(p.join(dir_path, 'out'))


if __name__ == '__main__':
    chdir()
    print('DIRECTORY: ')
    print(shell('pwd'))
    print('...........')
    result = shell('./output/eye ./compiler/tests/regression/inputs/hello_world.eye')
