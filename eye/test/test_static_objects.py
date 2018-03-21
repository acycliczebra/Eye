import logging
import json
import unittest

import compiler


class TestStaticObjects(unittest.TestCase):

    def test_classes(self):
        test = r'''def __main__ [args]{
            cls = class {
                static {
                    def foo 42
                }

                def __init__[self] {
                    print("HI!")
                }
            }
        }
        '''

        alt = r'''def __main__ [args]{
            cls = {
                def foo 42

                def __class__ class {
                    def __init__[self] {
                        print("HI!")
                    }
                }
            }
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

    def test_functions(self):
        test = r'''def __main__ [args]{
            f = [x]{
                static {
                    def foo 42
                }

                42
            }
        }
        '''

        alt = r'''def __main__ [args]{
            f = {
                def foo 42

                __function__ = [x]{
                    42
                }
            }
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)


if __name__ == '__main__':
    unittest.main()