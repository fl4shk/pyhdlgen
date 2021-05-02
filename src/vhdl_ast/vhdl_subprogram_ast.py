#!/usr/bin/env python3

#--------
from misc_util import *

#from vhdl_ast.vhdl_misc_ast import *
##from vhdl_ast.vhdl_expr_ast import *
#from vhdl_ast.vhdl_named_val_ast import *
#from vhdl_ast.vhdl_behav_ast import *
#from vhdl_ast.vhdl_type_ast import *

import vhdl_ast.vhdl_ast as vhdl_ast

from enum import Enum, auto
#--------
class SubprogramBase(vhdl_ast.Base, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, param_list=vhdl_ast.NamedObjList(),
		decls=vhdl_ast.NamedObjList(), body=vhdl_ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(param_list, vhdl_ast.NamedObjList), \
			type(param_list)
		self.__param_list = param_list

		assert isinstance(decls, vhdl_ast.NamedObjList), \
			type(decls)
		self.__decls = decls

		assert isinstance(body, vhdl_ast.NamedObjList), \
			type(body)
		self.__body = body
		#--------
	#--------
	def param_list(self):
		return self.__param_list
	def decls(self):
		return self.__decls
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitSubprogramBase(self)
	#--------
class Procedure(SubprogramBase):
	#--------
	def __init__(self, param_list=vhdl_ast.NamedObjList(),
		decls=vhdl_ast.NamedObjList(), body=vhdl_ast.NamedObjList(), *,
		name="", src_loc_at=1):
		super().__init__(param_list, decls, body, name=name,
			src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitProcedure(self)
	#--------
	def call(self, assoc_list):
		return vhdl_ast.CallProcedure(self, assoc_list)
	#--------
class Function(SubprogramBase):
	#--------
	class Kind(Enum):
		Pure = auto()
		Impure = auto()
	#--------
	def __init__(self, ret_type, param_list=vhdl_ast.NamedObjList(),
		decls=vhdl_ast.NamedObjList(), body=vhdl_ast.NamedObjList(),
		kind="pure", is_op=False, *, name="", src_loc_at=1):
		#--------
		super().__init__(param_list, decls, body, name=name,
			src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(ret_type, vhdl_ast.InstableTypeBase), \
			type(ret_type)
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
		return vhdl_ast.CallFunction(self, assoc_list)
	#--------
#--------
