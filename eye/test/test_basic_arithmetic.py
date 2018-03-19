import logging
import json
import unittest

import compiler


class TestBasicArithmetic(unittest.TestCase):

    def test_standard(self):

        expected = {
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
                                "type": "assignment_statement",
                                "to": {
                                    "type": "id",
                                    "value": "foo"
                                },
                                "value": {
                                    "type": "number",
                                    "value": "4"
                                }
                            },
                            {
                                "type": "function_call_expression",
                                "function": "print",
                                "parameters": [
                                    {
                                        "type": "id",
                                        "value": "foo"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }

        test = '''
        def __main__ [args]{
            foo = 4
            print(foo)
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_two_plus_two(self):

        expected = {
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
                                "type": "assignment_statement",
                                "to": {
                                    "type": "id",
                                    "value": "foo"
                                },
                                "value": {
                                    "type": "function_call_expression",
                                    "function": "__add__",
                                    "parameters": [
                                        {
                                            "type": "number",
                                            "value": "2"
                                        },
                                        {
                                            "type": "number",
                                            "value": "2"
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "function_call_expression",
                                "function": "print",
                                "parameters": [
                                    {
                                        "type": "id",
                                        "value": "foo"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }


        test = '''
        def __main__ [args]{
            foo = 2 + 2
            print(foo)
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        #print(json.dumps(result, indent=2))

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()