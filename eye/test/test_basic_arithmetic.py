import logging
import json
import unittest

import eyescript as compiler


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

    def test_plus(self):

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

    def test_multiply(self):


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
                                    "function": "__mul__",
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
            foo = 2 * 2
            print(foo)
        }
        '''

        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_division(self):


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
                                    "function": "__div__",
                                    "parameters": [
                                        {
                                            "type": "number",
                                            "value": "5"
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
            foo = 5 / 2
            print(foo)
        }
        '''
        result = compiler.compile(test)


        self.assertEqual(result, expected)


    def test_division(self):


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
                                    "function": "__sub__",
                                    "parameters": [
                                        {
                                            "type": "number",
                                            "value": "9"
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
            foo = 9 - 2
            print(foo)
        }
        '''

        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_many_plus(self):

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
                                            "type": "function_call_expression",
                                            "function": "__add__",
                                            "parameters": [
                                                {
                                                    "type": "function_call_expression",
                                                    "function": "__add__",
                                                    "parameters": [
                                                        {
                                                            "type": "number",
                                                            "value": "1"
                                                        },
                                                        {
                                                            "type": "number",
                                                            "value": "2"
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "number",
                                                    "value": "3"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "number",
                                            "value": "4"
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
            foo = 1 + 2 + 3 + 4
            print(foo)
        }
        '''

        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_many_products(self):

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
                                    "function": "__mul__",
                                    "parameters": [
                                        {
                                            "type": "function_call_expression",
                                            "function": "__mul__",
                                            "parameters": [
                                                {
                                                    "type": "function_call_expression",
                                                    "function": "__mul__",
                                                    "parameters": [
                                                        {
                                                            "type": "number",
                                                            "value": "1"
                                                        },
                                                        {
                                                            "type": "number",
                                                            "value": "2"
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "number",
                                                    "value": "3"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "number",
                                            "value": "4"
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
            foo = 1 * 2 * 3 * 4
            print(foo)
        }
        '''

        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_many_plus_and_minus(self):


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
                                            "type": "function_call_expression",
                                            "function": "__add__",
                                            "parameters": [
                                                {
                                                    "type": "function_call_expression",
                                                    "function": "__sub__",
                                                    "parameters": [
                                                        {
                                                            "type": "number",
                                                            "value": "1"
                                                        },
                                                        {
                                                            "type": "number",
                                                            "value": "2"
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "number",
                                                    "value": "1"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "number",
                                            "value": "5"
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
            foo = 1 - 2 + 1 + 5
            print(foo)
        }
        '''

        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_precedence(self):

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
                                            "type": "function_call_expression",
                                            "function": "__mul__",
                                            "parameters": [
                                                {
                                                    "type": "number",
                                                    "value": "3"
                                                },
                                                {
                                                    "type": "number",
                                                    "value": "2"
                                                }
                                            ]
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
            foo = 2 + 3 * 2
            print(foo)
        }
        '''

        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, expected)

    def test_brackets(self):

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
                                    "function": "__mul__",
                                    "parameters": [
                                        {
                                            "type": "function_call_expression",
                                            "function": "__add__",
                                            "parameters": [
                                                {
                                                    "type": "number",
                                                    "value": "2"
                                                },
                                                {
                                                    "type": "number",
                                                    "value": "3"
                                                }
                                            ]
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
            foo = (2 + 3) * 2
            print(foo)
        }
        '''

        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_brackets_right_side(self):

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
                                    "function": "__mul__",
                                    "parameters": [
                                        {
                                            "type": "number",
                                            "value": "2"
                                        },
                                        {
                                            "type": "function_call_expression",
                                            "function": "__add__",
                                            "parameters": [
                                                {
                                                    "type": "number",
                                                    "value": "2"
                                                },
                                                {
                                                    "type": "number",
                                                    "value": "3"
                                                }
                                            ]
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
            foo = 2 * (2 + 3)
            print(foo)
        }
        '''

        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_everything(self):
        test = '''
        def __main__ [args]{
            foo = (2 + 3 * (4 - 2)) * (bar(2) + qux(2 + 5)) * (7 / 3 / 2) * ((2 + 40) + (12 - 1))
            print(foo)
        }
        '''



if __name__ == '__main__':
    unittest.main()