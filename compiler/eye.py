#! /usr/bin/python3


import eye

test = '''
def __main__[args] {
    print("Hello World")
}
'''

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
            "type": "function_call_statment",
            "function": "print",
            "parameters": [
              {
                "type": "string_literal",
                "value": "Hello World"
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
    call
}'''


if __name__ == '__main__':
    eye.compile(test)
