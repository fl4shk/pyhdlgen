#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_expr_ast import *

from enum import Enum, auto
#--------
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
		assert left.is_lhs(), \
			type(left)
		self.__left = left

		Expr.assert_valid(right)
		self.__right = Literal.cast_maybe(right)
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
#--------
class ForStmt(BehavStmt):
	#--------
	def __init__(self, var_name, rang, stmts=[], *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__var_name = var_name
		self.__rang = rang
		self.__stmts = stmts
		#--------
	#--------
	def var_name(self):
		return self.__var_name
	def rang(self):
		return self.__rang
	def stmts(self):
		return self.__stmts
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
	def __init__(self, cond, stmts=[], *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__cond = cond
		self.__stmts = stmts
		#--------
	#--------
	def cond(self):
		return self.__cond
	def stmts(self):
		return self.__stmts
	#--------
	def visit(self, visitor):
		visitor.visitNodeIf(self)
	#--------
class NodeElsif(Base):
	#--------
	def __init__(self, cond, stmts=[], *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__cond = cond
		self.__stmts = stmts
		#--------
	#--------
	def cond(self):
		return self.__cond
	def stmts(self):
		return self.__stmts
	#--------
	def visit(self, visitor):
		visitor.visitNodeElsif(self)
	#--------
class NodeElse(Base):
	def __init__(self, stmts=[], *, src_loc_at=1)
		super().__init__(src_loc_at=src_loc_at + 1)
		self.__stmts = stmts
	def stmts(self):
		return self.__stmts
	def visit(self, visitor):
		visitor.visitNodeElse(self)
#--------