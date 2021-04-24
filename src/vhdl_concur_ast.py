#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_expr_ast import *

from enum import Enum, auto
#--------
# For `isinstance`
class ConcurStmtBase(Base):
	#--------
	def __init__(self, *, name="", src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		# `name` is the label name
		self._set_name(name)
	#--------
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitConcurrentStmtBase(self)
	#--------
#--------
class ConcurAssignStmt(ConcurStmtBase):
	#--------
	def __init__(self, left, right, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
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
		visitor.visitConcurAssignStmt(self)
	#--------
class ConcurSelAssignStmt(ConcurStmtBase):
	#--------
	def __init__(self, expr, left, sel_waves, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
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
		visitor.visitConcurSelAssignStmt(self)
	#--------
#--------
# To make `isinstance(obj, GenerateStmt)` work
class GenerateStmt(ConcurStmtBase):
	def __init__(self, *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitGenerateStmt(self)
class ForGenerateStmt(GenerateStmt):
	#--------
	def __init__(self, var_name, rang, body=[], *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
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
		visitor.visitForGenerateStmt(self)
	#--------
class IfGenerateStmt(GenerateStmt):
	def __init__(self, nodes=[], *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		visitor.visitIfGenerateStmt(self)
class CaseGenerateStmt(GenerateStmt):
	def __init__(self, nodes=[], *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		visitor.visitCaseGenerateStmt(self)
#--------
class BlockStmt(ConcurStmtBase):
#--------
