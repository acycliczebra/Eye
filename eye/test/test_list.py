import logging
import json
import unittest

import compiler


class TestList(unittest.TestCase):

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
                                    "type": "list",
                                    "value": [
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
            foo = [4]
            print(foo)
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_standard_multiple_items(self):

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
                                    "type": "list",
                                    "value": [
                                        {
                                            "type": "number",
                                            "value": "1"
                                        },
                                        {
                                            "type": "number",
                                            "value": "4"
                                        },
                                        {
                                            "type": "number",
                                            "value": "9"
                                        },
                                        {
                                            "type": "number",
                                            "value": "16"
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
            foo = [1, 4, 9, 16]
            print(foo)
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, expected)

    def test_from_function(self):
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
                                "function": "print",
                                "parameters": [
                                    {
                                        "type": "list",
                                        "value": [
                                            {
                                                "type": "number",
                                                "value": "4"
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
            print([4])
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)


        self.assertEqual(result, expected)

    def test_empty_list(self):
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
                                "function": "print",
                                "parameters": [
                                    {
                                        "type": "list",
                                        "value": [
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
            print([])
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)


        self.assertEqual(result, expected)



    def test_from_function_various_types(self):
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
                                "function": "print",
                                "parameters": [
                                    {
                                        "type": "list",
                                        "value": [
                                            {
                                                "type": "number",
                                                "value": "4"
                                            },
                                            {
                                                "type": "string",
                                                "value": "\"Four\""
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
            print([4, "Four"])
        }
        '''
        #logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, expected)