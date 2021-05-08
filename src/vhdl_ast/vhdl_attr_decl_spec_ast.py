#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
class AttrDecl(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, typ, *, name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(typ, InstableTypeBase), \
			type(typ)
		self.__typ = typ
		#--------
	#--------
	def typ(self):
		return self.__typ
	#--------
	def visit(self, visitor):
		visitor.visitAttrDecl(self)
	#--------
#--------
class AttrSpec(ast.Base):
	#--------
	def __init__(self, attr, obj_lst, expr, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(attr, AttrDecl), \
			type(attr)
		self.__attr = attr

		assert isinstance(obj_lst, list), \
			type(obj_lst)
		for i in range(len(obj_lst)):
			obj = obj_lst[i]
			assert isinstance(obj, AttrDecl), \
				psconcat("{}, {}, {}".format(i, obj, type(obj)))

		self.__obj_lst = obj_lst

		ast.Expr.assert_valid(expr)
		self.__expr = ast.BasicLiteral.cast_opt(expr)
		#--------
	#--------
	def attr(self):
		return self.__attr
	def obj_lst(self):
		return self.__obj_lst
	def expr(self):
		return self.__expr
	#--------
	def visit(self, visitor):
		visitor.visitAttrSpec(self)
	#--------
#--------
