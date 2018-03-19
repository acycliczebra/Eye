import logging
import json
import unittest

import compiler


class TestCurrying(unittest.TestCase):

    def test_standard(self):

        test = '''
        def __main__ [args]{
            foo(a, b, c)
        }
        '''

        test = '''
        def __main__ [args]{
            foo(a)(b)(c)
        }
        '''

        test = '''
        def __main__ [args]{
            foo(a)(bar(b))
        }
        '''

        test = '''
        def __main__ [args]{
            foo(bar(qux(a)))
        }
        '''

        test = '''
        def __main__ [args]{
            foo(bar(a), qux(b))
        }
        '''

        test = '''
        def __main__ [args]{
            [x]{ print(x) }(a)
        }
        '''

        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()