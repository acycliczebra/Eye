import logging
import json
import unittest

import compiler


class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        self.expected = {
            "version": "0.0.1",
            "statements": [
              {
                "type": "declaration_statement",
                "name": "__main__",
                "value": {
                  "type": "lambda_expression",
                  "args": [
                      "args"
                  ],
                  "statements": [
                    {
                      "type": "function_call_expression",
                      "function": "print",
                      "parameters": [
                        {
                          "type": "string",
                          "value": "\"Hello World\""
                        }
                      ]
                    }
                  ]
                }
              }
            ]
          }

    def test_standard(self):
        test = r'''def __main__ [args]{
            print("Hello World")
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)

    def test_one_line(self):
        test = r'''def __main__ [args]{print("Hello World")}
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)

    def test_one_line_with_spaces(self):
        test = r'''def __main__ [args]{ print("Hello World") }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)

    def test_one_strange_spacing(self):
        test = r'''def __main__ [args]{
            print("Hello World") }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)

    def test_trailing_newline(self):
        test = r'''def __main__ [args]{
            print("Hello World")
        }

        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)

    def test_leading_newline(self):
        test = r'''


        def __main__ [args]{
            print("Hello World")
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)

    def test_no_newlines(self):
        test = r'''def __main__ [args]{
            print("Hello World")
        }'''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)


"""
def test_no_args_standard(self):
    test = r'''def __main__ []{
        print("Hello World")
    }
    '''

    result = compiler.compile(test)

    self.assertEqual(result, self.expected)
"""

if __name__ == '__main__':
    unittest.main()