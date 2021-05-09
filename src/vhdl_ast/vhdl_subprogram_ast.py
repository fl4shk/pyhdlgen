#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
class SubprogramBase(ast.Base, ast.HasNameBase, ast.DslBehavBase):
	#--------
	def __init__(self, param_list=ast.NamedObjList(),
		decls=ast.NamedObjList(), body=ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		ast.DslBehavBase.__init__(self, body=body)
		#--------
		assert isinstance(param_list, ast.NamedObjList), \
			do_type_assert_psconcat(param_list)
		self.__param_list = param_list

		assert isinstance(decls, ast.NamedObjList), \
			do_type_assert_psconcat(decls)
		self.__decls = decls
		#--------
	#--------
	def param_list(self):
		return self.__param_list
	def decls(self):
		return self.__decls
	#--------
	def visit(self, visitor):
		visitor.visitSubprogramBase(self)
	#--------
class Procedure(SubprogramBase):
	#--------
	def __init__(self, param_list=ast.NamedObjList(),
		decls=ast.NamedObjList(), body=ast.NamedObjList(), *,
		name="", src_loc_at=1):
		super().__init__(param_list, decls, body, name=name,
			src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitProcedure(self)
	#--------
	def call(self, assoc_list):
		return ast.CallProcedure(self, assoc_list)
	#--------
class Function(SubprogramBase):
	#--------
	class Kind(Enum):
		Pure = auto()
		Impure = auto()
	#--------
	def __init__(self, ret_type, param_list=ast.NamedObjList(),
		decls=ast.NamedObjList(), body=ast.NamedObjList(),
		kind="pure", is_op=False, *, name="", src_loc_at=1):
		#--------
		super().__init__(param_list, decls, body, name=name,
			src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(ret_type, ast.InstableTypeBase), \
			do_type_assert_psconcat(ret_type)
		self.__ret_type = ret_type

		Kind = Function.Kind

		STR_KIND_MAP \
			= {
				"pure": Kind.Pure,
				"impure": Kind.Impure,
			}

		self.__kind = convert_str_to_enum_opt(kind, Kind, STR_KIND_MAP)

		self.__is_op = is_op
		#--------
	#--------
	def ret_type(self):
		return self.__ret_type
	def kind(self):
		return self.__kind
	def is_op(self):
		return self.__is_op
	#--------
	def visit(self, visitor):
		visitor.visitFunction(self)
	#--------
	def call(self, assoc_list):
		return ast.CallFunction(self, assoc_list)
	#--------
#--------
