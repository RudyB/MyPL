"""
Author: Rudy Bermudez
Filename: parser.py
Assignment: HW5
Description: Controls Parsing Tasks
"""

import mytoken
from error import Error
from mypl_ast import *


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
        stmt_list_node = StmtList()
        self.__advance()
        self.__stmts(stmt_list_node)
        self.__expect(mytoken.EOS, 'expecting end of file')
        return stmt_list_node

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

    def __stmts(self, stmt_list_node):
        """ Recursively calls `__stmt` and itself
        :param stmt_list_node: Accepts an instance of StmtList()
        """
        if not (self.current_token.tokentype == mytoken.EOS
                or self.current_token.tokentype == mytoken.END
                or self.current_token.tokentype == mytoken.ELSE
                or self.current_token.tokentype == mytoken.ELSEIF
                ):
            self.__stmt(stmt_list_node)
            self.__stmts(stmt_list_node)

    def __stmt(self, stmt_list_node):
        """ Recursively calls method for respective token type
        :param stmt_list_node: Accepts an instance of StmtList()
        """
        if self.current_token.tokentype == mytoken.PRINT or self.current_token.tokentype == mytoken.PRINTLN:
            self.__output(stmt_list_node)
        elif self.current_token.tokentype == mytoken.ID:
            self.__assign(stmt_list_node)
        elif self.current_token.tokentype == mytoken.IF:
            self.__cond(stmt_list_node)
        elif self.current_token.tokentype == mytoken.WHILE:
            self.__loop(stmt_list_node)

    def __output(self, stmt_list_node):
        """ Appends a PrintStmt() to `stmt_list_node`
        :param stmt_list_node: Accepts an instance of StmtList()
        """
        print_node = PrintStmt()
        if self.current_token.tokentype == mytoken.PRINT:
            print_node.is_println = False
            self.__advance()
            self.__expect(mytoken.LPAREN, 'expecting "("')
            print_node.expr = self.__expr()
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__expect(mytoken.SEMICOLON, 'expecting ";"')
            stmt_list_node.stmts.append(print_node)

        elif self.current_token.tokentype == mytoken.PRINTLN:
            print_node.is_println = True
            self.__advance()
            self.__expect(mytoken.LPAREN, 'expecting "("')
            print_node.expr = self.__expr()
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__expect(mytoken.SEMICOLON, 'expecting ";"')
            stmt_list_node.stmts.append(print_node)

    def __input(self):
        """ Returns an instantiated ReadExpr() with token is input related
        :return: An instance of ReadExpr()
        """
        read_node = ReadExpr()
        if self.current_token.tokentype == mytoken.READINT:
            read_node.is_read_int = True
            self.__advance()
            self.__expect(mytoken.LPAREN, 'expecting "("')
            read_node.msg = self.current_token
            self.__expect(mytoken.STRING, 'expecting "STRING"')
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__value()
            return read_node

        elif self.current_token.tokentype == mytoken.READSTR:
            self.__advance()
            read_node.is_read_int = False
            self.__expect(mytoken.LPAREN, 'expecting "("')
            read_node.msg = self.current_token
            self.__expect(mytoken.STRING, 'expecting "STRING"')
            self.__expect(mytoken.RPAREN, 'expecting ")"')
            self.__value()
            return read_node

    def __assign(self, stmt_list_node):
        """ Appends an AssignStmt() to `stmt_list_node`
        :param stmt_list_node:
        """
        assign_node = AssignStmt()
        assign_node.lhs = self.current_token
        self.__advance()
        assign_node.index_expr = self.__listindex()
        self.__expect(mytoken.ASSIGN, 'expecting "="')
        assign_node.rhs = self.__expr()
        self.__expect(mytoken.SEMICOLON, 'expecting ";"')
        stmt_list_node.stmts.append(assign_node)

    def __listindex(self):
        """ Returns an Expr() if the current pattern matches a List pattern. Else returns None
        :return: Either Expr() or None
        """
        if self.current_token.tokentype == mytoken.LBRACKET:
            self.__advance()
            expr = self.__expr()
            self.__expect(mytoken.RBRACKET, 'expecting "]"')
            return expr
        else:
            return None

    def __listindexid(self, simple_expr_node):
        """ Returns either an IndexExpr() if the current pattern matches a List pattern
            else returns `simple_expr_node`
        :param simple_expr_node: An Instance of SimpleExpr()
        :return: Returns either an IndexExpr() or SimpleExpr()
        """
        if self.current_token.tokentype == mytoken.LBRACKET:
            self.__advance()
            index_expr = IndexExpr()
            index_expr.identifier = simple_expr_node.term
            index_expr.expr = self.__expr()
            self.__expect(mytoken.RBRACKET, 'expecting "]"')
            return index_expr
        else:
            return simple_expr_node

    def __expr(self):
        """ Recursively calls `__value()` and returns `__exprt()`
        :return: A node of `__exprt()`
        """
        expr_node = self.__value()
        return self.__exprt(expr_node)

    def __value(self):
        """ Matches a tokentype to an Expr type
        :return: Returns an instance of Expr()
        """
        if self.current_token.tokentype == mytoken.ID:
            simple_expr_node = SimpleExpr()
            simple_expr_node.term = self.current_token
            self.__advance()
            node = self.__listindexid(simple_expr_node)
            return node

        elif (self.current_token.tokentype == mytoken.STRING
              or self.current_token.tokentype == mytoken.INT
              or self.current_token.tokentype == mytoken.BOOL
              ):
            simple_expr_node = SimpleExpr()
            simple_expr_node.term = self.current_token
            self.__advance()
            return simple_expr_node

        elif self.current_token.tokentype == mytoken.LBRACKET:
            self.__advance()
            # There is a chance that the list could be empty
            # In this case you want to check if the token after advancing is a RBRACKET
            # If it is a RBRACKET, eat the bracket and return empty ListExpr
            if self.current_token.tokentype == mytoken.RBRACKET:
                self.__expect(mytoken.RBRACKET, 'expecting "]"')
                return ListExpr()
            # Otherwise, you will return the List of Expressions
            else:
                list_expr = self.__exprlist()
                self.__expect(mytoken.RBRACKET, 'expecting "]"')
                return list_expr
        else:
            return self.__input()

    def __exprt(self, simple_expr):
        """ Checks to see if the `simple_expr` is a ComplexExpr()
        :param simple_expr: Instance of SimpleExpr()
        :return: either a SimpleExpr() or ComplexExpr()
        """
        if (self.current_token.tokentype == mytoken.PLUS
            or self.current_token.tokentype == mytoken.MINUS
            or self.current_token.tokentype == mytoken.DIVIDE
            or self.current_token.tokentype == mytoken.MULTIPLY
            or self.current_token.tokentype == mytoken.MODULUS
            ):
            complex_rel = ComplexExpr()
            complex_rel.first_operand = simple_expr
            complex_rel.math_rel = self.current_token
            self.__math_rel()   # Literally just advances
            complex_rel.rest = self.__expr()
            return complex_rel
        else:
            return simple_expr

    def __exprlist(self):
        """ Creates a ListExpr
        :return: An Instance of ListExpr()
        """
        expr_list = ListExpr()
        expr = self.__expr()
        expr_list.expressions.append(expr)
        self.__exprtail(expr_list)
        return expr_list

    def __exprtail(self, expr_list):
        """ Appends Expr() to `expr_list`
        :param expr_list: An instance of ListExpr()
        """
        if self.current_token.tokentype == mytoken.COMMA:
            self.__advance()
            expr_list.expressions.append(self.__expr())
            self.__exprtail(expr_list)

    def __math_rel(self):
        """ Advances current_token if Math Relation """
        self.__advance()

    def __cond(self, stmt_list_node):
        """ Appends an IfStmt() to `stmt_list_node`
        :param stmt_list_node: Instance of StmtList
        """
        if_stmt_node = IfStmt()
        self.__advance()
        if_stmt_node.if_part.bool_expr = self.__bexpr()
        self.__expect(mytoken.THEN, 'expecting "THEN"')
        self.__stmts(if_stmt_node.if_part.stmt_list)
        self.__condt(if_stmt_node)
        self.__expect(mytoken.END, 'expecting "END"')
        stmt_list_node.stmts.append(if_stmt_node)

    def __condt(self, if_stmt_node):
        """ Appends BasicIf() to `if_stmt_node` and handles ELSE Tokens
        :param if_stmt_node: Instance of IfStmt()
        """
        if self.current_token.tokentype == mytoken.ELSEIF:
            basic_if = BasicIf()
            self.__advance()
            basic_if.bool_expr = self.__bexpr()
            self.__expect(mytoken.THEN, 'expecting "THEN"')
            self.__stmts(basic_if.stmt_list)
            if_stmt_node.elseifs.append(basic_if)
            self.__condt(if_stmt_node)
        elif self.current_token.tokentype == mytoken.ELSE:
            if_stmt_node.has_else = True
            self.__advance()
            self.__stmts(if_stmt_node.else_stmts)

    def __bexpr(self):
        """ Handles Simple Boolean Expressions
        :return: An Instance of SimpleBoolExpr()
        """
        simple_bool_expr = SimpleBoolExpr()
        if self.current_token.tokentype == mytoken.NOT:
            simple_bool_expr.negated = True
            self.__advance()
            simple_bool_expr.expr = self.__expr()
            return self.__bexprt(simple_bool_expr)
        else:
            simple_bool_expr.negated = False
            simple_bool_expr.expr = self.__expr()
            return self.__bexprt(simple_bool_expr)

    def __bexprt(self, simple_bool_expr):
        """ Checks to see if `simple_bool_expr` is actually a ComplexBoolExpr()
        :param simple_bool_expr: Instance of SimpleBoolExpr()
        :return: `simple_bool_expr` if SimpleBoolExpr() or ComplexBoolExpr() otherwise
        """
        if (self.current_token.tokentype == mytoken.EQUAL
            or self.current_token.tokentype == mytoken.LESS_THAN
            or self.current_token.tokentype == mytoken.GREATER_THAN
            or self.current_token.tokentype == mytoken.LESS_THAN_EQUAL
            or self.current_token.tokentype == mytoken.GREATER_THAN_EQUAL
            or self.current_token.tokentype == mytoken.NOT_EQUAL
            ):
            complex_bool_expr = ComplexBoolExpr()
            complex_bool_expr.negated = simple_bool_expr.negated
            complex_bool_expr.first_expr = simple_bool_expr.expr
            complex_bool_expr.bool_rel = self.current_token
            self.__bool_rel()
            complex_bool_expr.second_expr = self.__expr()
            return self.__bconnect(complex_bool_expr)
        else:
            return simple_bool_expr

    def __bconnect(self, complex_bool_expr):
        """ Handles Adding Boolean Connectors to ComplexBoolExpr()
        :param complex_bool_expr: Instance of ComplexBoolExpr()
        :return: Instance of ComplexBoolExpr()
        """
        if self.current_token.tokentype == mytoken.AND:
            complex_bool_expr.has_bool_connector = True
            complex_bool_expr.bool_connector = self.current_token
            self.__advance()
            complex_bool_expr.rest = self.__bexpr()
            return complex_bool_expr
        elif self.current_token.tokentype == mytoken.OR:
            complex_bool_expr.has_bool_connector = True
            complex_bool_expr.bool_connector = self.current_token
            self.__advance()
            complex_bool_expr.rest = self.__bexpr()
            return complex_bool_expr
        else:
            complex_bool_expr.has_bool_connector = False
            complex_bool_expr.bool_connector = None
            complex_bool_expr.rest = None
            return complex_bool_expr

    def __bool_rel(self):
        """ Advances current_token if Boolean Relation """
        self.__advance()

    def __loop(self, stmt_list_node):
        """ Handles While Loops. Appends a While Statement to `stmt_list_node`
        :param stmt_list_node: An Instance of StmtList()
        """
        while_stmt = WhileStmt()
        self.__advance()
        while_stmt.bool_expr = self.__bexpr()
        self.__expect(mytoken.DO, 'expecting "DO"')
        self.__stmts(while_stmt.stmt_list)
        self.__expect(mytoken.END, 'expecting "END"')
        stmt_list_node.stmts.append(while_stmt)
