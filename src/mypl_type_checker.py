from mypl_ast import Visitor
from mypl_symbol_table import *
import mytoken as token
from error import Error


class TypeChecker(Visitor):

    def __init__(self):
        """ Instantiates a Type Checker """
        self.sym_table = SymbolTable()
        self.current_type = None

    # visitor functions

    def visit_stmt_list(self, stmt_list):
        """ Called When StmtList.accept(self) is called
        :param stmt_list: Instance of Type StmtList
        """
        self.sym_table.push_environment()
        for stmt in stmt_list.stmts:
            stmt.accept(self)
        self.sym_table.pop_environment()

    def visit_simple_bool_expr(self, simple_bool_expr):
        """ Accepts the Expr of a BoolExpr"""
        simple_bool_expr.expr.accept(self)

    def visit_complex_bool_expr(self, complex_bool_expr):
        """ Checks that all variables within a complex bool expr are of the same type
        :param complex_bool_expr: Instance of ComplexBoolExpr()
        """
        complex_bool_expr.first_expr.accept(self)
        complex_bool_expr.second_expr.accept(self)
        if complex_bool_expr.has_bool_connector:
            complex_bool_expr.rest.accept(self)

    def visit_if_stmt(self, if_stmt):
        """ Type Checks a IFStmt()
        :param if_stmt: Instance of IfStmt()
        """
        if_stmt.if_part.bool_expr.accept(self)
        self.sym_table.push_environment()
        if_stmt.if_part.stmt_list.accept(self)
        self.sym_table.pop_environment()
        for elseif in if_stmt.elseifs:
            elseif.bool_expr.accept(self)
            self.sym_table.push_environment()
            elseif.stmt_list.accept(self)
            self.sym_table.pop_environment()
        if if_stmt.has_else:
            self.sym_table.push_environment()
            if_stmt.else_stmts.accept(self)
            self.sym_table.pop_environment()

    def visit_while_stmt(self, while_stmt):
        """ Type Checks a While Stmt
        :param while_stmt: Instance of WhileStmt
        """
        while_stmt.bool_expr.accept(self)
        self.sym_table.push_environment()
        while_stmt.stmt_list.accept(self)
        self.sym_table.pop_environment()

    def visit_print_stmt(self, print_stmt):
        """ Accepts the Expr of a PrintStmt """
        print_stmt.expr.accept(self)

    def visit_assign_stmt(self, assign_stmt):
        """ Compares the rhs to the lhs of an assign stmt to insure type safety
        :param assign_stmt: Instance of AssignStmt()
        """
        lhs = assign_stmt.lhs
        assign_stmt.rhs.accept(self)
        if lhs.tokentype == token.ID:
            lhs_lexeme = lhs.lexeme
            if self.sym_table.variable_exists(lhs_lexeme):
                lhs_type = self.sym_table.get_variable_type(lhs_lexeme)
                if self.current_type != lhs_type:
                    msg = "expecting " + lhs_type + " but got " + self.current_type
                    raise Error(msg, lhs.line, lhs.column)
            else:
                self.sym_table.add_variable(lhs_lexeme)
                self.sym_table.set_variable_type(lhs_lexeme, self.current_type)

    def visit_simple_expr(self, simple_expr):
        """ Insures that an ID exits in the symbol table and that the types match
        :param simple_expr: Instance of SimpleExpr()
        """
        term = simple_expr.term
        if term.tokentype == token.ID:
            if self.sym_table.variable_exists(term.lexeme):
                self.current_type = self.sym_table.get_variable_type(term.lexeme)
            else:
                msg = term.lexeme + " is used before it is defined"
                raise Error(msg, term.line, term.column)
        else:
            self.current_type = term.tokentype

    def visit_index_expr(self, index_expr):
        print "Visit Index Expr     ---     Un-implemented"

    def visit_list_expr(self, list_expr):
        print "Visit List Expr     ---     Un-implemented"

    def visit_read_expr(self, read_expr):
        """ Visits a read Expr and checks to make sure the types match
        :param read_expr: Instance of ReadExpr()
        """
        node = read_expr.msg
        if read_expr.is_read_int:
            if node.tokentype != token.STRING:
                msg = "expecting INT but got " + node.tokentype
                raise Error(msg, node.line, node.column)
            self.current_type = token.INT
        else:
            if node.tokentype != token.STRING:
                msg = "expecting STRING but got " + node.tokentype
                raise Error(msg, node.line, node.column)
            self.current_type = token.STRING

    def visit_complex_expr(self, complex_expr):
        """ Type checks a complex expr
        :param complex_expr: Instance of ComplexExpr()
        """
        complex_expr.rest.accept(self)
        rhs = self.current_type
        complex_expr.first_operand.accept(self)     # simple expr in curr type
        first_op = complex_expr.first_operand.term
        if self.current_type != rhs:
            msg = "expecting " + rhs + " but got " + self.current_type
            raise Error(msg, first_op.line, first_op.column)
