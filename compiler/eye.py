#! /usr/bin/python3


import eye


expected = '''
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

test = '''def __main__ [args]{
    print("Hello World")
}
'''


if __name__ == '__main__':
    eye.compile(test)
