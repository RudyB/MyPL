import lexer
import mytoken
from error import Error


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def parser(self):
        """succeeds if program is syntactically well-formed"""
        self.advance()
        self.stmts()
        self.eat(mytoken.EOS, 'expecting end of file')  # helper functions:

    def advance(self):
        self.current_token = self.lexer.next_token()

    def eat(self, tokentype, error_msg):
        if self.current_token.tokentype == tokentype:
            self.advance()
        else:
            self.error(error_msg)

    def error(self, error_msg):
        s = error_msg + ' found "' + self.current_token.lexeme + '"'
        l = self.current_token.line
        c = self.current_token.column
        raise Error(s,l,c)

    def parse(self):
        self.advance()
        self.stmts()
        self.eat(mytoken.EOS, 'expecting end of file')

    def stmt(self):

    def stmts(self):
        if self.current_token.tokentype == mytoken.PRINT:
            self.advance()
            self.eat(mytoken.LPAREN, 'expecting "("')
            self.expr()
            self.eat(mytoken.RPAREN, 'expecting ")"')
            self.eat(mytoken.SEMICOLON, 'expecting ";"')
            self.stmts()

        elif self.current_token.tokentype == mytoken.PRINTLN:
            self.advance()
            self.eat(mytoken.LPAREN, 'expecting "("')
            self.expr()
            self.eat(mytoken.RPAREN, 'expecting ")"')
            self.eat(mytoken.SEMICOLON, 'expecting ";"')
            self.stmts()

        elif self.current_token.tokentype == mytoken.ID:
            self.advance()
            self.listindex()
            self.eat(mytoken.ASSIGN, 'expecting "="')
            self.expr()
            self.eat(mytoken.SEMICOLON, 'expecting ";"')
            self.stmts()

        elif self.current_token.tokentype == mytoken.IF:
            self.advance()
            self.bexpr()
            self.eat(mytoken.THEN, 'expecting "THEN"')
            self.stmts()
            self.condt()
            self.eat(mytoken.END, 'expecting "END"')

        elif self.current_token.tokentype == mytoken.WHILE:
            self.advance()
            self.bexpr()
            self.eat(mytoken.DO, 'expecting "DO"')
            self.stmts()
            self.eat(mytoken.END, 'expecting "END"')

    def output(self):

    def input(self):

    def assign(self):

    def listindex(self):

    def expr(self):

    def exprt(self):

    def value(self):

    def exprlist(self):

    def exprtail(self):

    def math_rel(self):

    def cond(self):

    def condt(self):

    def bexpr(self):

    def bexprt(self):

    def bconnect(self):

    def bool_rel(self):

    def loop(self):


