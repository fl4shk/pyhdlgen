#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
# for `isinstance`
class BehavStmt(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, *, name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
	#--------
	def visit(self, visitor):
		visitor.visitBehav(self)
	#--------
#--------
class DslBehavBase:
	#--------
	def __init__(self, body=ast.NamedObjList()):
		#--------
		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
		self.__body = body

		self.__nodes = []
		#--------
	#--------
	def body(self):
		return self.__body
	#--------
	def append(self, val):
		assert isinstance(val, BehavStmt), \
			do_type_assert_psconcat(val)
		self.__nodes[-1].body() += val
	def __iadd__(self, val):
		assert (isinstance(val, list) or isinstance(val, BehavStmt)), \
			do_type_assert_psconcat(val)

		if isinstance(val, list):
			for elem in val:
				self.append(elem)
		else: # if isinstance(val, BehavStmt):
			self.append(val)
	#--------
	#class _ScopeCtxMgr:
	#	def __init__(self, nodes):
	#		self.__nodes = nodes
	#	def __enter__(self):
	#		return self.__nodes[-1]
	#	def __exit__(self, type, value, traceback):
	#		node = self.__nodes[-1]
	#		if isinstance(node, NodeIf):

	#def If(self, cond, *, name=""):
	#	self.__nodes.append(If(name=name))
	#	self.__nodes.append(NodeIf(cond))
	#	self.__nodes[-1]._set_parent(self.__nodes[-2])
	#	self.__nodes[-2].nodes() += self.__nodes[-1]
	#	return DslBehavBase._ScopeCtxMgr(self.__nodes)
	#def Elsif(self, cond):
	#--------
#--------
class Assign(BehavStmt):
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
		visitor.visitAssign(self)
	#--------
class SelAssign(BehavStmt):
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
		assert (isinstance(procedure, ast.SmplName)
			or isinstance(procedure, ast.SelName)
			or isinstance(procedure, ast.Procedure)), \
			do_type_assert_psconcat(procedure)
		self.__procedure = procedure

		#assert (assoc_list is None or isinstance(assoc_list, list)
		#	or isinstance(assoc_list, dict)), \
		#	do_type_assert_psconcat(assoc_list)
		assert isinstance(assoc_list, ast.AssocList), \
			do_type_assert_psconcat(assoc_list)
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
	def __init__(self, expr, body=ast.NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		ast.Expr.assert_valid(expr)
		self.__expr = ast.BasicLiteral.cast_opt(expr)

		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
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
		visitor.visitFor(self)
	#--------
class Next(BehavStmt):
	#--------
	def __init__(self, loop_label=None, cond=None, *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(loop_label, ast.SmplName), \
			do_type_assert_psconcat(loop_label)
		self.__loop_label = loop_label

		if cond is not None:
			ast.Expr.assert_valid(cond)
			self.__cond = ast.BasicLiteral.cast_opt(cond)
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
		assert isinstance(loop_label, ast.SmplName), \
			do_type_assert_psconcat(loop_label)
		self.__loop_label = loop_label

		if cond is not None:
			ast.Expr.assert_valid(cond)
			self.__cond = ast.BasicLiteral.cast_opt(cond)
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
			do_type_assert_psconcat(nodes)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
	def visit(self, visitor):
		return visitor.visitIf(self)

# This is for both `if` and `if ... generate`.
class NodeIf(ast.Base):
	#--------
	def __init__(self, cond, body=ast.NamedObjList(), *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		ast.Expr.assert_valid(cond)
		self.__cond = ast.BasicLiteral.cast_opt(cond)

		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
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
class NodeElsif(ast.Base):
	#--------
	def __init__(self, cond, body=ast.NamedObjList(), *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		ast.Expr.assert_valid(cond)
		self.__cond = ast.BasicLiteral.cast_opt(cond)

		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
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
class NodeElse(ast.Base):
	def __init__(self, body=ast.NamedObjList(), *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
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
			do_type_assert_psconcat(nodes)
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

class NodeCaseWhen(ast.Base):
	#--------
	def __init__(self, choices, body=ast.NamedObjList(), *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# One of the choices can be `Others`.
		assert isinstance(choices, list), \
			do_type_assert_psconcat(choices)
		self.__choices = choices

		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
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

		ast.Expr.assert_valid(expr)
		self.__expr = ast.BasicLiteral.cast_opt(expr)
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
		ast.Expr.assert_valid(expr)
		self.__expr = ast.BasicLiteral.cast_opt(expr)

		ast.Expr.assert_valid(severity_expr)
		self.__severity_expr = ast.BasicLiteral.cast_opt \
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
