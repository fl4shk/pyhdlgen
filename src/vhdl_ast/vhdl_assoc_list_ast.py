#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast
#--------
# Association list
class AssocList(ast.Base):
	#--------
	def __init__(self, data, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert (data is None or isinstance(data, list)
			or isinstance(data, dict)), \
			do_type_assert_psconcat(data)

		self.__data = data
	#--------
	def data(self):
		return self.__data
	#--------
	def visit(self):
		visitor.visitAssocList(self)
	#--------
	def assert_valid(self, assert_valid_elem):
		if isinstance(data, list):
			for elem in data:
				assert_valid_elem(elem)
		elif isinstance(data, dict):
			for key in data:
				val = data[key]

				assert isinstance(key, str), \
					do_type_assert_psconcat(key)
				assert_valid_elem(val)
	#--------
#--------
class GenericMap(ast.Base):
	def __init__(self, assoc_list, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(assoc_list, AssocList), \
			do_type_assert_psconcat(assoc_list)

		def assert_valid_elem(elem):
			assert isinstance(elem, ast.Expr), \
				do_type_assert_psconcat(elem)
		assoc_list.assert_valid(assert_valid_elem)

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

		def assert_valid_elem(elem):
			assert (isinstance(elem, ast.Expr)
				or isinstance(elem, Open)), \
				do_type_assert_psconcat(elem)
		assoc_list.assert_valid(assert_valid_elem)

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
