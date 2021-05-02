#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast
#--------
# Simple name
class SmplName(ast.Base):
	def __init__(self, val, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(val, str), \
			type(val)
		self.__val = val
	def val(self):
		return self.__val
	def visit(self, visitor):
		visitor.visitSmplName(self)
# Selected names, used for `Use`
class SelName(ast.Base):
	#--------
	def __init__(self, lst, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(lst, list), \
			type(lst)
		assert len(lst) > 1, \
			psconcat("len, lst:  {}, {}".format(len(lst), lst))

		for i in range(len(lst) - 1):
			assert (isinstance(lst[i], SmplName)
				or isinstance(lst[i], ast.CallFunction)), \
				type(lst[i])
		assert (isinstance(lst[-1], SmplName)
			or isinstance(lst[-1], ast.CharLiteral)
			or isinstance(lst[-1], ast.StrLiteral)
			or isinstance(lst[-1], ast.All)), \
			type(lst[-1])
		#--------
	#--------
	def lst(self):
		return self.__lst
	#--------
	def visit(self, visitor):
		visitor.visitSelName(self)
	#--------
	@staticmethod
	def cast_simple(to_cast):
		assert isinstance(to_cast, str), \
			type(to_cast)
		lst = [elem.lower() for elem in to_cast.split(".")]
		if lst[-1] == "all":
			lst[-1] = All()

		assert len(lst) > 1, \
			psconcat("len, lst:  {}, {}".format(len(lst), lst))

		for i in range(len(lst) - 1):
			lst[i] = SmplName(lst[i])

		return SelName(lst)
	#--------
#--------
