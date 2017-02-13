"""
Author: Rudy Bermudez
Filename: parser.py
Assignment: HW3
Description: Controls Parsing Tasks
"""

import mytoken
from error import Error


class Parser(object):

    def __init__(self, lexer):
        """ Initializes the Parser Class
        :param lexer: Instance of `Lexer`
        """
        self.lexer = lexer
        self.current_token = None

    def parse(self):
        """ Starts the reverse descent parser

        Succeeds if program is syntactically well-formed
        """
        self.__advance()
        self.__stmts()
        self.__expect(mytoken.EOS, 'expecting end of file')

    def __advance(self):
        """ Calls for the next token from the `lexer` and stores it to `self.current_token` """
        self.current_token = self.lexer.next_token()

    def __expect(self, tokentype, error_msg):
        """ Checks to see if the current token is what is syntactically expected
        :param tokentype: the expected token type of type `Token`
        :param error_msg: the error message to be delivered to the console
        """
        if self.current_token.tokentype == tokentype:
            self.__advance()
        else:
            self.__error(error_msg)

    def __error(self, error_msg):
        """ Raises an Error
        :param error_msg: the error message to be delivered to the console
        """
        s = error_msg + ' found "' + self.current_token.lexeme + '"'
        l = self.current_token.line
        c = self.current_token.column
        raise Error(s, l, c)

    def __stmts(self):
        if not (self.current_token.tokentype == mytoken.EOS
                or self.current_token.tokentype == mytoken.END
                or self.current_token.tokentype == mytoken.ELSE
                or self.current_token.tokentype == mytoken.ELSEIF
                ):
            self.__stmt()
            self.__stmts()

    def __stmt(self):
        if self.current_token.tokentype == mytoken.PRINT or self.current_token.tokentype == mytoken.PRINTLN:
            self.__output()
        elif self.current_token.tokentype == mytoken.ID:
            self.__assign()
        elif self.current_token.tokentype == mytoken.IF:
            self.__cond()
        elif self.current_token.tokentype == mytoken.WHILE:
            self.__loop()

    def __output(self):
        if self.current_token.tokentype == mytoken.PRINT:
            self.__advance()
            self.__expect(mytoken.LPAREN, 'expecting "("')
            self.__expr()
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__expect(mytoken.SEMICOLON, 'expecting ";"')

        elif self.current_token.tokentype == mytoken.PRINTLN:
            self.__advance()
            self.__expect(mytoken.LPAREN, 'expecting "("')
            self.__expr()
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__expect(mytoken.SEMICOLON, 'expecting ";"')

    def __input(self):
        if self.current_token.tokentype == mytoken.READINT:
            self.__advance()
            self.__expect(mytoken.LPAREN, 'expecting "("')
            self.__expect(mytoken.STRING, 'expecting "STRING"')
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__value()

        elif self.current_token.tokentype == mytoken.READSTR:
            self.__advance()
            self.__expect(mytoken.LPAREN, 'expecting "("')
            self.__expect(mytoken.STRING, 'expecting "STRING"')
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__value()

    def __assign(self):
        self.__advance()
        self.__listindex()
        self.__expect(mytoken.ASSIGN, 'expecting "="')
        self.__expr()
        self.__expect(mytoken.SEMICOLON, 'expecting ";"')

    def __listindex(self):
        if self.current_token.tokentype == mytoken.LBRACKET:
            self.__advance()
            self.__expr()
            self.__expect(mytoken.RBRACKET, 'expecting "]"')

    def __expr(self):
        self.__value()
        self.__exprt()

    def __exprt(self):
        if (self.current_token.tokentype == mytoken.PLUS
            or self.current_token.tokentype == mytoken.MINUS
            or self.current_token.tokentype == mytoken.DIVIDE
            or self.current_token.tokentype == mytoken.MULTIPLY
            or self.current_token.tokentype == mytoken.MODULUS
            ):
            self.__math_rel()
            self.__expr()

    def __value(self):
        if self.current_token.tokentype == mytoken.ID:
            self.__advance()
            self.__listindex()
        elif (self.current_token.tokentype == mytoken.STRING
              or self.current_token.tokentype == mytoken.INT
              or self.current_token.tokentype == mytoken.BOOL
              ):
            self.__advance()
        elif self.current_token.tokentype == mytoken.LBRACKET:
            self.__advance()
            self.__exprlist()
            self.__expect(mytoken.RBRACKET, 'expecting "]"')
        else:
            self.__input()

    def __exprlist(self):
        # TODO: Do I have to do a nested check of <expr> and <value> ?
        self.__expr()
        self.__exprtail()

    def __exprtail(self):
        if self.current_token.tokentype == mytoken.COMMA:
            self.__advance()
            self.__expr()
            self.__exprtail()

    def __math_rel(self):
        self.__advance()

    def __cond(self):
        self.__advance()
        self.__bexpr()
        self.__expect(mytoken.THEN, 'expecting "THEN"')
        self.__stmts()
        self.__condt()
        self.__expect(mytoken.END, 'expecting "END"')

    def __condt(self):
        if self.current_token.tokentype == mytoken.ELSEIF:
            self.__advance()
            self.__bexpr()
            self.__expect(mytoken.THEN, 'expecting "THEN"')
            self.__stmts()
            self.__condt()
        elif self.current_token.tokentype == mytoken.ELSE:
            self.__advance()
            self.__stmts()

    def __bexpr(self):
        if self.current_token.tokentype == mytoken.NOT:
            self.__advance()
            self.__expr()
            self.__bexprt()
        else:
            self.__expr()
            self.__bexprt()

    def __bexprt(self):
        if (self.current_token.tokentype == mytoken.EQUAL
            or self.current_token.tokentype == mytoken.LESS_THAN
            or self.current_token.tokentype == mytoken.GREATER_THAN
            or self.current_token.tokentype == mytoken.LESS_THAN_EQUAL
            or self.current_token.tokentype == mytoken.GREATER_THAN_EQUAL
            or self.current_token.tokentype == mytoken.NOT_EQUAL
            ):
            self.__bool_rel()
            self.__expr()
            self.__bconnect()

    def __bconnect(self):
        if self.current_token.tokentype == mytoken.AND:
            self.__advance()
            self.__bexpr()
        elif self.current_token.tokentype == mytoken.OR:
            self.__advance()
            self.__bexpr()

    def __bool_rel(self):
        self.__advance()

    def __loop(self):
        self.__advance()
        self.__bexpr()
        self.__expect(mytoken.DO, 'expecting "DO"')
        self.__stmts()
        self.__expect(mytoken.END, 'expecting "END"')
