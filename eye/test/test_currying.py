import logging
import json
import unittest

import compiler


class TestCurrying(unittest.TestCase):

    def test_simple_function_call(self):

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
                                "type": "function_call_expression",
                                "function": "foo",
                                "parameters": [
                                    {
                                        "type": "id",
                                        "value": "a"
                                    },
                                    {
                                        "type": "id",
                                        "value": "b"
                                    },
                                    {
                                        "type": "id",
                                        "value": "c"
                                    },
                                ]
                            }
                        ]
                    }
                }
            ]
        }

        test = '''
        def __main__ [args]{
            foo(a, b, c)
        }
        '''

        result = compiler.compile(test)
        self.assertEqual(result, expected)

    def test_currying(self):

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
                                "type": "function_call_expression",
                                "function": {
                                    "type": "function_call_expression",
                                    "function": {
                                        "type": "function_call_expression",
                                        "function": "foo",
                                        "parameters": [
                                            {
                                                "type": "id",
                                                "value": "a"
                                            },
                                        ]
                                    },
                                    "parameters": [
                                        {
                                            "type": "id",
                                            "value": "b"
                                        },
                                    ]
                                },
                                "parameters": [
                                    {
                                        "type": "id",
                                        "value": "c"
                                    },
                                ]
                            }
                        ]
                    }
                }
            ]
        }

        test = '''
        def __main__ [args]{
            foo(a)(b)(c)
        }
        '''

        result = compiler.compile(test)
        self.assertEqual(result, expected)

    def test_function_call_in_parameter(self):

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
                                "type": "function_call_expression",
                                "function": "foo",
                                "parameters": [
                                    {
                                        "type": "function_call_expression",
                                        "function": "bar",
                                        "parameters": [
                                            {
                                                "type": "function_call_expression",
                                                "function": "qux",
                                                "parameters": [
                                                    {
                                                        "type": "id",
                                                        "value": "a"
                                                    }
                                                ]
                                            }
                                        ]
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
            foo(bar(qux(a)))
        }
        '''

        result = compiler.compile(test)
        self.assertEqual(result, expected)

    def test_multiple_function_calls_in_parameter(self):

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
                                "type": "function_call_expression",
                                "function": "foo",
                                "parameters": [
                                    {
                                        "type": "function_call_expression",
                                        "function": "bar",
                                        "parameters": [
                                            {
                                                "type": "id",
                                                "value": "a"
                                            },
                                        ]
                                    },
                                    {
                                        "type": "function_call_expression",
                                        "function": "qux",
                                        "parameters": [
                                            {
                                                "type": "id",
                                                "value": "b"
                                            },
                                        ]
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
            foo(bar(a), qux(b))
        }
        '''

        result = compiler.compile(test)
        self.assertEqual(result, expected)

    def test_function_call_currying(self):

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
                                "type": "function_call_expression",
                                "function": {
                                    "type": "function_call_expression",
                                    "function": "foo",
                                    "parameters": [
                                        {
                                            "type": "id",
                                            "value": "a"
                                        }
                                    ]
                                },
                                "parameters": [
                                    {
                                        "type": "function_call_expression",
                                        "function": "bar",
                                        "parameters": [
                                            {
                                                "type": "id",
                                                "value": "b"
                                            },
                                        ]
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
            foo(a)(bar(b))
        }
        '''

        result = compiler.compile(test)
        self.assertEqual(result, expected)

    def test_immediately_invoked_function_expression(self):

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
                                "type": "function_call_expression",
                                "function": {
                                    "type": "lambda_expression",
                                    "args": [
                                        "x"
                                    ],
                                    "statements": [
                                        {
                                            "type": "function_call_expression",
                                            "function": "print",
                                            "parameters": [
                                                {
                                                    "type": "id",
                                                    "value": "x"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "parameters": [
                                    {
                                        "type": "id",
                                        "value": "a"
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
            [x]{ print(x) }(a)
        }
        '''

        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()