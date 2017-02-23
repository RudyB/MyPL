"""
Author: Rudy Bermudez
Filename: mytoken.py
Assignment: HW4
Description: Model class of a Token
"""


PRINT = 'PRINT'
PRINTLN = 'PRINTLN'
READINT = 'READINT'
READSTR = 'READSTR'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
SEMICOLON = 'SEMICOLON'
ID = 'ID'
LBRACKET = 'LBRACKET'
RBRACKET = 'RBRACKET'
STRING = 'STRING'
INT = 'INT'
BOOL = 'BOOL'
COMMA = 'COMMA'
ASSIGN = 'ASSIGN'
PLUS = 'PLUS'
MINUS = 'MINUS'
DIVIDE = 'DIVIDE'
MULTIPLY = 'MULTIPLY'
MODULUS = 'MODULUS'
IF = 'IF'
THEN = 'THEN'
ELSEIF = 'ELSEIF'
ELSE = 'ELSE'
END = 'END'
NOT = 'NOT'
AND = 'AND'
OR = 'OR'
EQUAL = 'EQUAL'
LESS_THAN = 'LESS_THAN'
GREATER_THAN = 'GREATER_THAN'
LESS_THAN_EQUAL = 'LESS_THAN_EQUAL'
GREATER_THAN_EQUAL = 'GREATER_THAN_EQUAL'
NOT_EQUAL = 'NOT_EQUAL'
WHILE = 'WHILE'
DO = 'DO'
EOS = 'EOS'


class Token(object):
    """ Model class of a Token

     :Parameters:
        - tokentype: The Type of Token
        - lexeme: The Lexeme of a Token
        - line: line of token
        - column: column of token

    """
    def __init__(self, tokentype, lexeme, line, column):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return "%s '%s' %s:%s" % (self.tokentype, self.lexeme, self.line, self.column)
