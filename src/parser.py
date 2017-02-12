import mytoken
from error import Error


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def parse(self):
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

    def stmts(self):
        if not (self.current_token.tokentype == mytoken.EOS
                or self.current_token.tokentype == mytoken.END
                or self.current_token.tokentype == mytoken.ELSE
                or self.current_token.tokentype == mytoken.ELSEIF
                ):
            self.stmt()
            self.stmts()

    def stmt(self):
        if self.current_token.tokentype == mytoken.PRINT or self.current_token.tokentype == mytoken.PRINTLN:
            self.output()
        elif self.current_token.tokentype == mytoken.ID:
            self.assign()
        elif self.current_token.tokentype == mytoken.IF:
            self.cond()
        elif self.current_token.tokentype == mytoken.WHILE:
            self.loop()

    def output(self):
        if self.current_token.tokentype == mytoken.PRINT:
            self.advance()
            self.eat(mytoken.LPAREN, 'expecting "("')
            self.expr()
            self.eat(mytoken.RPAREN, 'expecting ")"')
            self.eat(mytoken.SEMICOLON, 'expecting ";"')

        elif self.current_token.tokentype == mytoken.PRINTLN:
            self.advance()
            self.eat(mytoken.LPAREN, 'expecting "("')
            self.expr()
            self.eat(mytoken.RPAREN, 'expecting ")"')
            self.eat(mytoken.SEMICOLON, 'expecting ";"')

    def input(self):
        if self.current_token.tokentype == mytoken.READINT:
            self.advance()
            self.eat(mytoken.LPAREN, 'expecting "("')
            self.eat(mytoken.STRING, 'expecting "STRING"')
            self.eat(mytoken.RPAREN, 'expecting ")"')
            self.value()

        elif self.current_token.tokentype == mytoken.READSTR:
            self.advance()
            self.eat(mytoken.LPAREN, 'expecting "("')
            self.eat(mytoken.STRING, 'expecting "STRING"')
            self.eat(mytoken.RPAREN, 'expecting ")"')
            self.value()

    def assign(self):
        self.advance()
        self.listindex()
        self.eat(mytoken.ASSIGN, 'expecting "="')
        self.expr()
        self.eat(mytoken.SEMICOLON, 'expecting ";"')

    def listindex(self):
        if self.current_token.tokentype == mytoken.LBRACKET:
            self.advance()
            self.expr()
            self.eat(mytoken.RBRACKET,'expecting "]"')

    def expr(self):
        self.value()
        self.exprt()

    def exprt(self):
        if (self.current_token.tokentype == mytoken.PLUS or
                    self.current_token.tokentype == mytoken.MINUS or
                    self.current_token.tokentype == mytoken.DIVIDE or
                    self.current_token.tokentype == mytoken.MULTIPLY or
                    self.current_token.tokentype == mytoken.MODULUS
            ):
            self.math_rel()
            self.expr()

    def value(self):
        if self.current_token.tokentype == mytoken.ID:
            self.advance()
            self.listindex()
        elif (self.current_token.tokentype == mytoken.STRING or
                      self.current_token.tokentype == mytoken.INT or
                      self.current_token.tokentype == mytoken.BOOL
              ):
            self.advance()
        elif self.current_token.tokentype == mytoken.LBRACKET:
            self.advance()
            self.exprlist()
            self.eat(mytoken.RBRACKET,'expecting "]"')
        else:
            self.input()


    def exprlist(self):
        # TODO: DO I have to do a nested check of <expr> and <value>
        self.expr()
        self.exprtail()

    def exprtail(self):
        if self.current_token.tokentype == mytoken.COMMA:
            self.advance()
            self.expr()
            self.exprtail()

    def math_rel(self):
        self.advance()

    def cond(self):
        self.advance()
        self.bexpr()
        self.eat(mytoken.THEN, 'expecting "THEN"')
        self.stmts()
        self.condt()
        self.eat(mytoken.END, 'expecting "END"')

    def condt(self):
        if self.current_token.tokentype == mytoken.ELSEIF:
            self.advance()
            self.bexpr()
            self.eat(mytoken.THEN,'expecting "THEN"')
            self.stmts()
            self.condt()
        elif self.current_token.tokentype == mytoken.ELSE:
            self.advance()
            self.stmts()

    def bexpr(self):
        if self.current_token.tokentype == mytoken.NOT:
            self.advance()
            self.expr()
            self.bexprt()
        else:
            self.expr()
            self.bexprt()

    def bexprt(self):
        if (self.current_token.tokentype == mytoken.EQUAL or
                    self.current_token.tokentype == mytoken.LESS_THAN or
                    self.current_token.tokentype == mytoken.GREATER_THAN or
                    self.current_token.tokentype == mytoken.LESS_THAN_EQUAL or
                    self.current_token.tokentype == mytoken.GREATER_THAN_EQUAL or
                    self.current_token.tokentype == mytoken.NOT_EQUAL
            ):
            self.bool_rel()
            self.expr()
            self.bconnect()

    def bconnect(self):
        if self.current_token.tokentype == mytoken.AND:
            self.advance()
            self.bexpr()
        elif self.current_token.tokentype == mytoken.OR:
            self.advance()
            self.bexpr()

    def bool_rel(self):
        self.advance()

    def loop(self):
        self.advance()
        self.bexpr()
        self.eat(mytoken.DO, 'expecting "DO"')
        self.stmts()
        self.eat(mytoken.END, 'expecting "END"')


