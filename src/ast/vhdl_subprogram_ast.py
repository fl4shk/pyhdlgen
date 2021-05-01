#!/usr/bin/env python3

#--------
from misc_util import *

from vhdl_misc_ast import *
from vhdl_expr_ast import *
from vhdl_named_val_ast import *
from vhdl_behav_ast import *

from enum import Enum, auto()
#--------
class SubprogramBase(Base, HasNameBase):
	#--------
	def __init__(self, param_list=NamedObjList(), decls=NamedObjList(),
		body=NamedObjList(), *, name="", src_loc_at=1):
		#--------
		Base.__init__(self, src_loc_at=src_loc_at + 1)
		HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(param_list, NamedObjList), \
			type(param_list)
		self.__param_list = param_list

		assert isinstance(decls, NamedObjList), \
			type(decls)
		self.__decls = decls

		assert isinstance(body, NamedObjList), \
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
	def __init__(self, param_list=NamedObjList(), decls=NamedObjList(),
		body=NamedObjList(), *, name="", src_loc_at=1):
		super().__init__(param_list, decls, body, name=name,
			src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitProcedure(self)
	#--------
	def call(self, assoc_list):
		return CallProcedure(self, assoc_list)
	#--------
class Function(SubprogramBase):
	#--------
	class Kind(Enum):
		Pure = auto()
		Impure = auto()
	#--------
	def __init__(self, ret_type, kind="impure", param_list=NamedObjList(),
		decls=NamedObjList(), body=NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		super().__init__(param_list, decls, body, name=name,
			src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(ret_type, InstableTypeBase), \
			type(ret_type)
		self.__ret_type = ret_type

		Kind = Function.Kind

		STR_KIND_MAP \
			= {
				"pure": Kind.Pure,
				"impure": Kind.Impure,
			}

		self.__kind = convert_str_to_enum_opt(kind, Kind, STR_KIND_MAP)
		#--------
	#--------
	def ret_type(self):
		return self.__ret_type
	def kind(self):
		return self.__kind
	#--------
	def visit(self, visitor):
		visitor.visitFunction(self)
	#--------
	def call(self, assoc_list):
		return CallFunction(self, assoc_list)
	#--------
#--------
