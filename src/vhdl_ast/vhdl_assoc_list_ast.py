#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast
#--------
# Association list
class AssocList(ast.Base):
	def __init__(self, data, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert (data is None or isinstance(data, list)
			or isinstance(data, dict)), \
			do_type_assert_psconcat(data)
		self.__data = data
	def data(self):
		return self.__data
	def visit(self):
		visitor.visitAssocList(self)
#--------
class GenericMap(ast.Base):
	def __init__(self, assoc_list, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(assoc_list, AssocList), \
			do_type_assert_psconcat(assoc_list)
		self.__assoc_list = assoc_list
	def assoc_list(self):
		return self.__assoc_list
	def visit(self, visitor):
		visitor.visitGenericMap(self)
class PortMap(ast.Base):
	def __init__(self, assoc_list, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(assoc_list, AssocList), \
			do_type_assert_psconcat(assoc_list)
		self.__assoc_list = assoc_list
	def assoc_list(self):
		return self.__assoc_list
	def visit(self, visitor):
		visitor.visitPortMap(self)
#--------
class Open(ast.Base):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitOpen(self)
#--------
