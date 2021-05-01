#!/usr/bin/env python3

#--------
from misc_util import *

from vhdl_misc_ast import *
from vhdl_expr_ast import *
#--------
# Simple name
class SmplName(Base):
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
class SelName(Base):
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
				or isinstance(lst[i], SelName)
				or isinstance(lst[i], CallFunction)), \
				type(lst[i])
		assert (isinstance(lst[-1], SmplName)
			or isinstance(lst[-1], CharLiteral)
			or isinstance(lst[-1], StrLiteral)
			or isinstance(lst[-1], All)), \
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
