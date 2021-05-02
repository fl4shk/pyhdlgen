#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_ast.vhdl_misc_ast import *
##from vhdl_ast.vhdl_expr_ast import *
##from vhdl_ast.vhdl_named_val_ast import *
#from vhdl_ast.vhdl_assoc_list_ast import *
#from vhdl_ast.vhdl_subprogram_ast import *
#from vhdl_ast.vhdl_name_ast import *
#from vhdl_ast.vhdl_type_ast import *

import vhdl_ast.vhdl_ast as vhdl_ast

from enum import Enum, auto
#--------
# for `isinstance`
class BehavStmt(vhdl_ast.Base, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, *, name="", src_loc_at=1):
		#--------
		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
	#--------
	def visit(self, visitor):
		visitor.visitBehav(self)
	#--------
#--------
class Assign(BehavStmt):
	#--------
	def __init__(self, left, right, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(left, vhdl_ast.Expr), \
			type(left)
		assert left.is_lvalue(), \
			type(left)
		self.__left = left

		vhdl_ast.Expr.assert_valid(right)
		self.__right = vhdl_ast.BasicLiteral.cast_opt(right)
		#--------
	#--------
	def left(self):
		return self.__left
	def right(self):
		return self.__right
	#--------
	def visit(self, visitor):
		visitor.visitAssign(self)
	#--------
class SelAssign(BehavStmt):
	#--------
	def __init__(self, expr, left, sel_waves, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert vhdl_ast.Expr.is_valid(expr), \
			type(expr)
		self.__expr = vhdl_ast.BasicLiteral.cast_opt(expr)

		assert isinstance(left, vhdl_ast.Expr), \
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
		visitor.visitSelAssign(self)
	#--------
#--------
class CallProcedure(BehavStmt):
	#--------
	def __init__(self, procedure, assoc_list, *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert (isinstance(procedure, vhdl_ast.SmplName)
			or isinstance(procedure, vhdl_ast.SelName)
			or isinstance(procedure, vhdl_ast.Procedure)), \
			type(procedure)
		self.__procedure = procedure

		#assert (assoc_list is None or isinstance(assoc_list, list)
		#	or isinstance(assoc_list, dict)), \
		#	type(assoc_list)
		assert isinstance(assoc_list, vhdl_ast.AssocList), \
			type(assoc_list)
		self.__assoc_list = assoc_list
		#--------
	#--------
	def procedure(self):
		return self.__procedure
	def assoc_list(self):
		return self.__assoc_list
	#--------
	def visit(self, visitor):
		visitor.visitCallProcedure(self)
	#--------
#--------
class While(BehavStmt):
	#--------
	def __init__(self, expr, body=vhdl_ast.NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		vhdl_ast.Expr.assert_valid(expr)
		self.__expr = vhdl_ast.BasicLiteral.cast_opt(expr)

		assert isinstance(body, vhdl_ast.NamedObjList), \
			type(body)
		self.__body = body
		#--------
	#--------
	def expr(self):
		return self.__expr
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitWhile(self)
	#--------
class For(BehavStmt):
	#--------
	def __init__(self, var_name, rang, body=vhdl_ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(var_name, vhdl_ast.SmplName), \
			type(var_name)
		self.__var_name = var_name

		assert isinstance(rang, vhdl_ast.ConRangeBase), \
			type(rang)
		self.__rang = rang

		assert isinstance(body, vhdl_ast.NamedObjList), \
			type(body)
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
		visitor.visitFor(self)
	#--------
class Next(BehavStmt):
	#--------
	def __init__(self, loop_label=None, cond=None, *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(loop_label, vhdl_ast.SmplName), \
			type(loop_label)
		self.__loop_label = loop_label

		if cond is not None:
			vhdl_ast.Expr.assert_valid(cond)
			self.__cond = vhdl_ast.BasicLiteral.cast_opt(cond)
		else:
			self.__cond = cond
		#--------
	#--------
	def loop_label(self):
		return self.__loop_label
	def cond(self):
		return self.__cond
	#--------
	def visit(self, visitor):
		visitor.visitNext(self)
	#--------
class Exit(BehavStmt):
	#--------
	def __init__(self, loop_label=None, cond=None, *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(loop_label, vhdl_ast.SmplName), \
			type(loop_label)
		self.__loop_label = loop_label

		if cond is not None:
			vhdl_ast.Expr.assert_valid(cond)
			self.__cond = vhdl_ast.BasicLiteral.cast_opt(cond)
		else:
			self.__cond = cond
		#--------
	#--------
	def loop_label(self):
		return self.__loop_label
	def cond(self):
		return self.__cond
	#--------
	def visit(self, visitor):
		visitor.visitExit(self)
	#--------
#--------
class If(BehavStmt):
	def __init__(self, nodes=[], *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)

		assert isinstance(nodes, list), \
			type(nodes)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		return visitor.visitIf(self)

# This is for both `if` and `if ... generate`.
class NodeIf(vhdl_ast.Base):
	#--------
	def __init__(self, cond, body=vhdl_ast.NamedObjList(), *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		vhdl_ast.Expr.assert_valid(cond)
		self.__cond = vhdl_ast.BasicLiteral.cast_opt(cond)

		assert isinstance(body, vhdl_ast.NamedObjList), \
			type(body)
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
class NodeElsif(vhdl_ast.Base):
	#--------
	def __init__(self, cond, body=vhdl_ast.NamedObjList(), *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		vhdl_ast.Expr.assert_valid(cond)
		self.__cond = vhdl_ast.BasicLiteral.cast_opt(cond)

		assert isinstance(body, vhdl_ast.NamedObjList), \
			type(body)
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
class NodeElse(vhdl_ast.Base):
	def __init__(self, body=vhdl_ast.NamedObjList(), *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(body, vhdl_ast.NamedObjList), \
			type(body)
		self.__body = body
	def body(self):
		return self.__body
	def visit(self, visitor):
		visitor.visitNodeElse(self)
#--------
class Case(BehavStmt):
	#--------
	def __init__(self, is_qmark=False, nodes=[], *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		self.__is_qmark = is_qmark

		assert isinstance(nodes, list), \
			type(nodes)
		self.__nodes = nodes
		#--------
	#--------
	def is_qmark(self):
		return self.__is_qmark
	def nodes(self):
		return self.__nodes
	#--------
	def visit(self, visitor):
		visitor.visitCase(self)
	#--------

class NodeCaseWhen(vhdl_ast.Base):
	#--------
	def __init__(self, choices, body=vhdl_ast.NamedObjList(), *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# One of the choices can be `Others`.
		assert isinstance(choices, list), \
			type(choices)
		self.__choices = choices

		assert isinstance(body, vhdl_ast.NamedObjList), \
			type(body)
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
class Return(BehavStmt):
	def __init__(self, expr, *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)

		vhdl_ast.Expr.assert_valid(expr)
		self.__expr = vhdl_ast.BasicLiteral.cast_opt(expr)
	def expr(self):
		return self.__expr
	def visit(self):
		visitor.visitReturn(self)
#--------
class Null(BehavStmt):
	def __init__(self, *, name="", src_loc_at=1):
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitNull(self)
#--------
class Report(BehavStmt):
	#--------
	def __init__(self, expr, severity_expr, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		vhdl_ast.Expr.assert_valid(expr)
		self.__expr = vhdl_ast.BasicLiteral.cast_opt(expr)

		vhdl_ast.Expr.assert_valid(severity_expr)
		self.__severity_expr = vhdl_ast.BasicLiteral.cast_opt \
			(severity_expr)
		#--------
	#--------
	def expr(self):
		return self.__expr
	def severity_expr(self):
		return self.__severity_expr
	#--------
	def visit(self, visitor):
		visitor.visitReport(self)
	#--------
#--------
