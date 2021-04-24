#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_expr_ast import *

from enum import Enum, auto
#--------
# for `isinstance`
class BehavStmt(Base):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBehavStmt(self)
#--------
class AssignStmt(BehavStmt):
	#--------
	def __init__(self, left, right, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(left, Expr), \
			type(left)
		assert left.is_lvalue(), \
			type(left)
		self.__left = left

		Expr.assert_valid(right)
		self.__right = BasicLiteral.cast_opt(right)
		#--------
	#--------
	def left(self):
		return self.__left
	def right(self):
		return self.__right
	#--------
	def visit(self, visitor):
		visitor.visitAssignStmt(self)
	#--------
class SelAssignStmt(ConcurStmtBase):
	#--------
	def __init__(self, expr, left, sel_waves, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert Expr.is_valid(expr), \
			type(expr)
		self.__expr = BasicLiteral.cast_opt(expr)

		assert isinstance(left, Expr), \
			type(left)
		assert left.is_lvalue(), \
			type(left)
		self.__left = left

		self.__sel_waves = sel_waves
		#--------
	#--------
	def expr(self):
		return self.__expr
	def left(self):
		return self.__left
	def sel_waves(self):
		return self.__sel_waves
	#--------
	def visit(self, visitor):
		visitor.visitSelAssignStmt(self)
	#--------
#--------
class ForStmt(BehavStmt):
	#--------
	def __init__(self, var_name, rang, body=[], *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__var_name = var_name
		self.__rang = rang
		self.__body = body
		#--------
	#--------
	def var_name(self):
		return self.__var_name
	def rang(self):
		return self.__rang
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitForStmt(self)
	#--------
#--------
class IfStmt(BehavStmt):
	def __init__(self, nodes=[], *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		return visitor.visitIfStmt(self)

# This is for both `if` and `if ... generate`.
class NodeIf(Base):
	#--------
	def __init__(self, cond, body=[], *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__cond = cond
		self.__body = body
		#--------
	#--------
	def cond(self):
		return self.__cond
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitNodeIf(self)
	#--------
class NodeElsif(Base):
	#--------
	def __init__(self, cond, body=[], *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__cond = cond
		self.__body = body
		#--------
	#--------
	def cond(self):
		return self.__cond
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitNodeElsif(self)
	#--------
class NodeElse(Base):
	def __init__(self, body=[], *, src_loc_at=1)
		super().__init__(src_loc_at=src_loc_at + 1)
		self.__body = body
	def body(self):
		return self.__body
	def visit(self, visitor):
		visitor.visitNodeElse(self)
#--------
class CaseStmt(BehavStmt):
	def __init__(self, nodes=[], *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		visitor.visitCaseStmt(self)

class NodeCaseWhen(Base):
	#--------
	def __init__(self, choices, body=[], *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# One of the choices can be "others".
		self.__choices = choices
		self.__body = body
		#--------
	#--------
	def choices(self):
		return self.__choices
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitNodeCaseWhen(self)
	#--------
#--------
class ReportStmt(BehavStmt):
	#--------
	def __init__(self, expr, severity_expr, *, name="", src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		Expr.assert_valid(expr)
		self.__expr = BasicLiteral.cast_opt(expr)

		Expr.assert_valid(severity_expr)
		self.__severity_expr = BasicLiteral.cast_opt(severity_expr)

		self._set_name(name)
		#--------
	#--------
	def expr(self):
		return self.__expr
	def severity_expr(self):
		return self.__severity_expr
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitReportStmt(self)
	#--------
#--------
