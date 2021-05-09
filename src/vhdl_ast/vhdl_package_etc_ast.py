#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
class Package(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, decls=ast.NamedObjList(), is_extern=False, *,
		name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		#assert isinstance(generics, ast.NamedObjList), \
		#	do_type_assert_psconcat(generics)
		#self.__generics = generics

		assert isinstance(decls, ast.NamedObjList), \
			do_type_assert_psconcat(decls)
		self.__decls = decls

		self.__is_extern = is_extern
		#--------
	#--------
	#def generics(self):
	#	return self.__generics
	def decls(self):
		return self.__decls
	def is_extern(self):
		return self.__is_extern
	#--------
	def visit(self, visitor):
		visitor.visitPackage(self)
	#--------
class PackageBody(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, decls=ast.NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(decls, ast.NamedObjList), \
			do_type_assert_psconcat(decls)
		self.__decls = decls
		#--------
	#--------
	def decls(self):
		return self.__decls
	#--------
	def visit(self, visitor):
		visitor.visitPackageBody(self)
	#--------
class UseClause(ast.Base):
	def __init__(self, sel_name_lst=[], *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(sel_name_lst, list), \
			do_type_assert_psconcat(sel_name_lst)
		for sel_name in sel_name_lst:
			assert isinstance(sel_name, ast.SelName), \
				do_type_assert_psconcat(sel_name)

		self.__sel_name_lst = sel_name_lst
	def sel_name_lst(self):
		return self.__sel_name_lst
	def visit(self, visitor):
		visitor.visitUseClause(self)
class Library(ast.Base):
	def __init__(self, which, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(which, SmplName), \
			do_type_assert_psconcat(which)
		self.__which = which
	def which(self):
		return self.__which
	def visit(self, visitor):
		visitor.visitLibrary(self)
#--------
