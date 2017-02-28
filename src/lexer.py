"""
Author: Rudy Bermudez
Filename: lexer.py
Assignment: HW5
Description: Model class of a Lexer
"""

import mytoken
import error


class Lexer(object):
    """ Model class of a Lexer

    :Parameters:
        - input_stream: Instance of an input_stream that contains the contents of source code to analyze

    :Properties:
        - line: line of current symbol
        - column: column of current symbol

    """

    def __init__(self, input_stream):
        self.line = 1
        self.column = 0
        self.input_stream = input_stream

    def __peek(self):
        """ Returns the next character in the input_stream without changing the input_stream position """
        pos = self.input_stream.tell()
        symbol = self.input_stream.read(1)
        self.input_stream.seek(pos)
        return symbol

    def __read(self):
        """ Returns the next character in the input_stream and increments the input_stream position """
        return self.input_stream.read(1)

    def advance_column(self):
        """ Increments the column property by 1 """
        self.column += 1

    def advance_line(self):
        """ Increments the line by 1 and resets the column to 0 """
        self.column = 0
        self.line += 1

    def next_token(self):
        """
        Parses the current symbol from the input_stream and returns it's
        perspective Token

        If a token cannot be parsed, an error of Type Error will be raised
        """
        symbol = self.__read()
        self.advance_column()

        """ Checks to see if end of file has been reached and returns EOS Token """
        if symbol == '':
            return mytoken.Token(mytoken.EOS, "", self.line, self.column)

        """ Checks for a new line and then advances the line property """
        if symbol == '\n':
            self.advance_line()
            return self.next_token()

        """ Checks for a comment and then advances the input_stream until new line is found """
        if symbol == '#':
            go = True
            while go:
                if self.__peek() == '\n':
                    self.__read()
                    self.advance_line()
                    go = False
                else:
                    self.__read()
                    self.advance_column()
            return self.next_token()

        if symbol.isspace():
            return self.next_token()

        """ Checks for a digit and then returns an INT Token with the number as the lexeme """
        if symbol.isdigit():
            column_at_start = self.column
            line_at_start = self.line
            cur_num = symbol
            while self.__peek().isdigit():
                cur_num += self.__read()
                self.advance_column()
            return mytoken.Token(mytoken.INT, cur_num, line_at_start, column_at_start)

        """
        Checks if symbol is alphanumeric and iterates (while storing chars.) until next char is no longer alphanumeric
        Then matches characters against token types and returns respective token
        """
        if symbol.isalpha():
            column_at_start = self.column
            line_at_start = self.line
            cur_string = symbol
            while self.__peek().isalpha() or self.__peek().isdigit() or self.__peek() == '_':
                cur_string += self.__read()
                self.advance_column()

            if cur_string == 'println':
                return mytoken.Token(mytoken.PRINTLN, cur_string, line_at_start, column_at_start)
            if cur_string == 'print':
                return mytoken.Token(mytoken.PRINT, cur_string, line_at_start, column_at_start)
            if cur_string == 'while':
                return mytoken.Token(mytoken.WHILE, cur_string, line_at_start, column_at_start)
            if cur_string == 'if':
                return mytoken.Token(mytoken.IF, cur_string, line_at_start, column_at_start)
            if cur_string == 'end':
                return mytoken.Token(mytoken.END, cur_string, line_at_start, column_at_start)
            if cur_string == 'else':
                return mytoken.Token(mytoken.ELSE, cur_string, line_at_start, column_at_start)
            if cur_string == 'elseif':
                return mytoken.Token(mytoken.ELSEIF, cur_string, line_at_start, column_at_start)
            if cur_string == 'do':
                return mytoken.Token(mytoken.DO, cur_string, line_at_start, column_at_start)
            if cur_string == 'then':
                return mytoken.Token(mytoken.THEN, cur_string, line_at_start, column_at_start)
            if cur_string == 'readint':
                return mytoken.Token(mytoken.READINT, cur_string, line_at_start, column_at_start)
            if cur_string == 'readstr':
                return mytoken.Token(mytoken.READSTR, cur_string, line_at_start, column_at_start)
            if cur_string == 'and':
                return mytoken.Token(mytoken.AND, cur_string, line_at_start, column_at_start)
            if cur_string == 'or':
                return mytoken.Token(mytoken.OR, cur_string, line_at_start, column_at_start)
            if cur_string == 'not':
                return mytoken.Token(mytoken.NOT, cur_string, line_at_start, column_at_start)
            if cur_string == 'true' or cur_string == 'false':
                return mytoken.Token(mytoken.BOOL, cur_string, line_at_start, column_at_start)
            else:
                return mytoken.Token(mytoken.ID, cur_string, line_at_start, column_at_start)

        """
        Checks to see if symbol is a quotation and then iterates (while storing chars.) until last quotation is found
        Then returns the Token with the character as a lexeme
        """
        if symbol == '"':
            column_at_start = self.column
            line_at_start = self.line
            go = True
            cur_string = ''
            while go:
                if self.__peek() == '\n':
                    raise error.Error("reached newline reading string", self.line, self.column)
                if self.__peek() == '"':
                    self.__read()
                    self.advance_column()
                    go = False
                else:
                    cur_string += self.__read()
                    self.advance_column()
            return mytoken.Token(mytoken.STRING, cur_string, line_at_start, column_at_start)

        if symbol == '=':
            if self.__peek() == '=':
                self.__read()
                self.advance_column()
                return mytoken.Token(mytoken.EQUAL, '==', self.line, self.column)
            else:
                return mytoken.Token(mytoken.ASSIGN, '=', self.line, self.column)

        if symbol == '<':
            if self.__peek() == '=':
                self.__read()
                self.advance_column()
                return mytoken.Token(mytoken.LESS_THAN_EQUAL, '<=', self.line, self.column)

            else:
                return mytoken.Token(mytoken.LESS_THAN, '<', self.line, self.column)

        if symbol == '>':
            if self.__peek() == '=':
                self.__read()
                self.advance_column()
                return mytoken.Token(mytoken.GREATER_THAN_EQUAL, '>=', self.line, self.column)

            else:
                return mytoken.Token(mytoken.GREATER_THAN, '>', self.line, self.column)

        if symbol == '!':
            if self.__peek() == '=':
                self.__read()
                self.advance_column()
                return mytoken.Token(mytoken.NOT_EQUAL, '!=', self.line, self.column)

        if symbol == ',':
            return mytoken.Token(mytoken.COMMA, ',', self.line, self.column)

        if symbol == ';':
            cur_line = self.line
            cur_column = self.column
            return mytoken.Token(mytoken.SEMICOLON, ';', cur_line, cur_column)

        """
        Mathematical Lexemes
        """
        if symbol == '+':
            return mytoken.Token(mytoken.PLUS, '+', self.line, self.column)

        if symbol == '-':
            return mytoken.Token(mytoken.MINUS, '-', self.line, self.column)

        if symbol == '*':
            return mytoken.Token(mytoken.MULTIPLY, '*', self.line, self.column)

        if symbol == '/':
            return mytoken.Token(mytoken.DIVIDE, '/', self.line, self.column)

        if symbol == '%':
            return mytoken.Token(mytoken.MODULUS, '%', self.line, self.column)

        """
        Brackets and Parenthesis
        """
        if symbol == '[':
            return mytoken.Token(mytoken.LBRACKET, '[', self.line, self.column)

        if symbol == ']':
            return mytoken.Token(mytoken.RBRACKET, ']', self.line, self.column)

        if symbol == '(':
            return mytoken.Token(mytoken.LPAREN, '(', self.line, self.column)

        if symbol == ')':
            return mytoken.Token(mytoken.RPAREN, ')', self.line, self.column)

        else:

            """
            In the case that the symbol cannot be parsed into a token,
            An error is raised with the symbol that caused the error embedded in the message
            """
            raise error.Error("'%s' could not be parsed" % symbol, self.line, self.column)
