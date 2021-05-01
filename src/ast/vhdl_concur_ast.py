#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_expr_ast import *

from enum import Enum, auto
#--------
# For `isinstance()`
class ConcurStmtBase(Base, HasNameBase):
	#--------
	def __init__(self, *, name="", src_loc_at=1):
		Base.__init__(self, src_loc_at=src_loc_at + 1)

		# `name` is the label name
		HasNameBase.__init__(self, name=name)
	#--------
	def visit(self, visitor):
		visitor.visitConcurrentStmtBase(self)
	#--------
#--------
class ConcurAssign(ConcurStmtBase):
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
		visitor.visitConcurAssign(self)
	#--------
class ConcurSelAssign(ConcurStmtBase):
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
		visitor.visitConcurSelAssign(self)
	#--------
#--------
# To make `isinstance(obj, GenerateStmtBase)` work
class GenerateStmtBase(ConcurStmtBase):
	def __init__(self, *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitGenerateStmt(self)
class ForGenerate(GenerateStmtBase):
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
		visitor.visitForGenerate(self)
	#--------
class IfGenerate(GenerateStmtBase):
	def __init__(self, nodes=[], *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		visitor.visitIfGenerate(self)
class CaseGenerate(GenerateStmtBase):
	def __init__(self, nodes=[], *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		visitor.visitCaseGenerate(self)
#--------
class Block(ConcurStmtBase):
	#--------
	def __init__(self, generics=NamedObjList(), generic_map=None,
		ports=NamedObjList(), port_map=None, body=NamedObjList(),
		guard_cond=None, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		self.__generics = generics

		assert (generic_map is None
			or isinstance(generic_map, GenericMap)), \
			type(generic_map)
		self.__generic_map = generic_map

		self.__ports = ports

		assert (port_map is None or isinstance(port_map, PortMap)), \
			type(port_map)
		self.__port_map = port_map

		assert isinstance(body, NamedObjList)
		self.__body = body

		assert isinstance(guard_cond, Expr), \
			type(guard_cond)
		self.__guard_cond = guard_cond
		#--------
	#--------
	def generics(self):
		return self.__generics
	def generic_map(self):
		return self.__generic_map
	def ports(self):
		return self.__ports
	def port_map(self):
		return self.__port_map
	def body(self):
		return self.__body
	def guard_cond(self):
		return self.__guard_cond
	#--------
	def visit(self, visitor):
		visitor.visitBlock(self)
	#--------
#--------
class Process(ConcurStmtBase):
	#--------
	def __init__(self, sens_lst=[], decls=NamedObjList(),
		body=NamedObjList(), *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert (isinstance(sens_lst, list) or isinstance(sens_lst, All)), \
			type(sens_lst)
		self.__sens_lst = sens_lst

		assert isinstance(decls, NamedObjList), \
			type(decls)
		self.__decls = decls

		assert isinstance(body, NamedObjList), \
			type(body)
		self.__body = body
		#--------
	#--------
	def sens_lst(self):
		return self.__sens_lst
	def decls(self):
		return self.__decls
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitProcess(self)
	#--------
#--------
