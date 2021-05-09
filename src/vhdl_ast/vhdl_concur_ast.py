#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
# For `isinstance()`
class ConcurStmtBase(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, *, name="", src_loc_at=1):
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)

		# `name` is the label name
		ast.HasNameBase.__init__(self, name=name)
	#--------
	def visit(self, visitor):
		visitor.visitConcurrentStmtBase(self)
	#--------
#--------
class DslConcurBase:
	#--------
	#class 
	#--------
#--------
class ConcurAssign(ConcurStmtBase):
	#--------
	def __init__(self, left, right, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(left, ast.Expr), \
			do_type_assert_psconcat(left)
		assert left.is_lvalue(), \
			do_type_assert_psconcat(left)
		self.__left = left

		ast.Expr.assert_valid(right)
		self.__right = ast.BasicLiteral.cast_opt(right)
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
		assert ast.Expr.is_valid(expr), \
			do_type_assert_psconcat(expr)
		self.__expr = ast.BasicLiteral.cast_opt(expr)

		assert isinstance(left, ast.Expr), \
			do_type_assert_psconcat(left)
		assert left.is_lvalue(), \
			do_type_assert_psconcat(left)
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
	def __init__(self, var_name, rang, body=ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(var_name, ast.SmplName), \
			do_type_assert_psconcat(var_name)
		self.__var_name = var_name

		assert isinstance(rang, ast.ConRangeBase), \
			do_type_assert_psconcat(rang)
		self.__rang = rang

		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
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

		assert isinstance(nodes, list), \
			do_type_assert_psconcat(nodes)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		visitor.visitIfGenerate(self)
class CaseGenerate(GenerateStmtBase):
	def __init__(self, nodes=[], *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)

		assert isinstance(nodes, list), \
			do_type_assert_psconcat(nodes)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		visitor.visitCaseGenerate(self)
#--------
class Block(ConcurStmtBase):
	#--------
	def __init__(self, generics=ast.NamedObjList(), generic_map=None,
		ports=ast.NamedObjList(), port_map=None,
		body=ast.NamedObjList(), guard_cond=None, *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		self.__generics = generics

		assert (generic_map is None
			or isinstance(generic_map, GenericMap)), \
			do_type_assert_psconcat(generic_map)
		self.__generic_map = generic_map

		self.__ports = ports

		assert (port_map is None or isinstance(port_map, PortMap)), \
			do_type_assert_psconcat(port_map)
		self.__port_map = port_map

		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
		self.__body = body

		#assert isinstance(guard_cond, ast.Expr), \
		#	do_type_assert_psconcat(guard_cond)

		ast.Expr.assert_valid(guard_cond)
		self.__guard_cond = ast.BasicLiteral.cast_opt(guard_cond)
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
class Process(ConcurStmtBase, ast.DslBehavBase):
	#--------
	def __init__(self, sens_lst=[], decls=ast.NamedObjList(),
		body=ast.NamedObjList(), *, name="", src_loc_at=1):
		#--------
		ConcurStmtBase.__init__(self, name=name, src_loc_at=src_loc_at + 1)
		ast.DslBehavBase.__init__(self, body)
		#--------
		assert (isinstance(sens_lst, list) or isinstance(sens_lst, All)), \
			do_type_assert_psconcat(sens_lst)
		self.__sens_lst = sens_lst

		assert isinstance(decls, ast.NamedObjList), \
			do_type_assert_psconcat(decls)
		self.__decls = decls
		#--------
	#--------
	def sens_lst(self):
		return self.__sens_lst
	def decls(self):
		return self.__decls
	#--------
	def visit(self, visitor):
		visitor.visitProcess(self)
	#--------
#--------
