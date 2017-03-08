from mypl_ast import Visitor
from mypl_symbol_table import SymbolTable
import mytoken as token
import sys


class Interpreter(Visitor):

    def __init__(self):
        self.sym_table = SymbolTable()  # var_name -> value
        self.current_value = None  # last evaluation result
        self.flag = False

    def visit_stmt_list(self, stmt_list):
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
        temp = self.current_value
        complex_bool_expr.second_expr.accept(self)
        if complex_bool_expr.negated:
            if complex_bool_expr.bool_rel.tokentype == token.EQUAL:
                if self.current_value == temp:
                    self.flag = False
                else:
                    self.flag = True
            elif complex_bool_expr.bool_rel.tokentype == token.NOT_EQUAL:
                if self.current_value == temp:
                    self.flag = True
                else:
                    self.flag = False
            elif complex_bool_expr.bool_rel.tokentype == token.GREATER_THAN:
                if temp > self.current_value:
                    self.flag = False
                else:
                    self.flag = True
            elif complex_bool_expr.bool_rel.tokentype == token.GREATER_THAN_EQUAL:
                if temp >= self.current_value:
                    self.flag = False
                else:
                    self.flag = True
            elif complex_bool_expr.bool_rel.tokentype == token.LESS_THAN:
                if temp < self.current_value:
                    self.flag = False
                else:
                    self.flag = True
            elif complex_bool_expr.bool_rel.tokentype == token.LESS_THAN_EQUAL:
                if temp <= self.current_value:
                    self.flag = False
                else:
                    self.flag = True
        else:
            if complex_bool_expr.bool_rel.tokentype == token.EQUAL:
                if self.current_value == temp:
                    self.flag = True
                else:
                    self.flag = False
            elif complex_bool_expr.bool_rel.tokentype == token.NOT_EQUAL:
                if self.current_value == temp:
                    self.flag = False
                else:
                    self.flag = True
            elif complex_bool_expr.bool_rel.tokentype == token.GREATER_THAN:
                if temp > self.current_value:
                    self.flag = True
                else:
                    self.flag = False
            elif complex_bool_expr.bool_rel.tokentype == token.GREATER_THAN_EQUAL:
                if temp >= self.current_value:
                    self.flag = True
                else:
                    self.flag = False
            elif complex_bool_expr.bool_rel.tokentype == token.LESS_THAN:
                if temp < self.current_value:
                    self.flag = True
                else:
                    self.flag = False
            elif complex_bool_expr.bool_rel.tokentype == token.LESS_THAN_EQUAL:
                if temp <= self.current_value:
                    self.flag = True
                else:
                    self.flag = False

        if complex_bool_expr.has_bool_connector:
            complex_bool_expr.rest.accept(self)

    def visit_if_stmt(self, if_stmt):
        """ Type Checks a IFStmt()
        :param if_stmt: Instance of IfStmt()
        """
        has_executed = False
        if_stmt.if_part.bool_expr.accept(self)

        if self.flag:
            has_executed = True
            if_stmt.if_part.stmt_list.accept(self)
        for elseif in if_stmt.elseifs:
            elseif.bool_expr.accept(self)
            if self.flag:
                has_executed = True
                self.sym_table.push_environment()
                elseif.stmt_list.accept(self)
                self.sym_table.pop_environment()
        if not has_executed:
            if if_stmt.has_else:
                if_stmt.else_stmts.accept(self)

    def visit_while_stmt(self, while_stmt):
        """ Type Checks a While Stmt
        :param while_stmt: Instance of WhileStmt
        """
        self.flag = True
        while self.flag:
            while_stmt.bool_expr.accept(self)
            if self.flag:
                while_stmt.stmt_list.accept(self)
            else:
                break

    def visit_assign_stmt(self, assign_stmt):
        """ Compares the rhs to the lhs of an assign stmt to insure type safety
        :param assign_stmt: Instance of AssignStmt()
        """
        lhs = assign_stmt.lhs
        assign_stmt.rhs.accept(self)
        if lhs.tokentype == token.ID:
            lhs_lexeme = lhs.lexeme
            if self.sym_table.variable_exists(lhs_lexeme):
                self.sym_table.set_variable_value(lhs_lexeme, self.current_value)
            else:
                self.sym_table.add_variable(lhs_lexeme)
                self.sym_table.set_variable_value(lhs_lexeme, self.current_value)

    def visit_simple_expr(self, simple_expr):
        if simple_expr.term.tokentype == token.ID:
            var_name = simple_expr.term.lexeme
            var_val = self.sym_table.get_variable_value(var_name)
            self.current_value = var_val
        elif simple_expr.term.tokentype == token.INT:
            self.current_value = int(simple_expr.term.lexeme)
        elif simple_expr.term.tokentype == token.BOOL:
            if simple_expr.term.lexeme == "true":
                self.current_value = True
            else:
                self.current_value = False
        elif simple_expr.term.tokentype == token.STRING:
            self.current_value = simple_expr.term.lexeme

    def __write(self, msg):
        sys.stdout.write(str(msg))

    def visit_print_stmt(self, print_stmt):
        print_stmt.expr.accept(self)
        if type(self.current_value) == bool:
            if self.current_value:
                self.__write("true")
            else:
                self.__write("false")
        else:
            self.__write(self.current_value)
        if print_stmt.is_println:
            self.__write('\n')

    def visit_read_expr(self, read_expr):
        val = raw_input(read_expr.msg.lexeme)
        if read_expr.is_read_int:
            try:
                self.current_value = int(val)
            except ValueError:
                self.current_value = 0
        else:
            self.current_value = val

    def visit_complex_expr(self, complex_expr):
        """ Type checks a complex expr
        :param complex_expr: Instance of ComplexExpr()
        """
        complex_expr.rest.accept(self)
        var_value = self.current_value
        complex_expr.first_operand.accept(self)     # simple expr in curr type
        math_rel = complex_expr.math_rel.tokentype
        if math_rel == token.PLUS:
            self.current_value += var_value
        elif math_rel == token.MINUS:
            self.current_value -= var_value
        elif math_rel == token.MULTIPLY:
            self.current_value *= var_value
        elif math_rel == token.DIVIDE:
            self.current_value /= var_value
        elif math_rel == token.MODULUS:
            self.current_value %= var_value