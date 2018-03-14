import logging
import json
import unittest

import compiler


class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        json_source = r'''
          {
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
                      "type": "function_call_statement",
                      "function": {
                        "type": "id",
                        "value": "print"
                      },
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
        '''


        self.expected_json = json.loads(json_source)
        self.expected = json.dumps(self.expected_json, indent=2)

    def test_standard(self):
        test = r'''def __main__ [args]{
            print("Hello World")
        }
        '''

        logging.basicConfig(level=logging.DEBUG)
        result = compiler.compile(test)

        self.assertEqual(result, self.expected)


if __name__ == '__main__':
    unittest.main()