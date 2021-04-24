#!/usr/bin/env python3

#--------
from misc_util import *

from vhdl_misc_ast import *
from vhdl_expr_ast import *
from vhdl_type_ast import *

from enum import Enum, auto
#--------
#class Generic(Base):
#	#--------
#	class Kind(Enum):
#		Null = auto()
#		Constant = auto()
#		Type = auto()
#		Function = auto()
#		Procedure = auto()
#	#--------
#	def __init__(self, kind, typ, def_val=None, *, name="", src_loc_at=1):
#		#--------
#		super().__init__(src_loc_at=src_loc_at + 1)
#		#--------
#		Kind = Generic.Kind
#		assert (isinstance(kind, Kind) or isinstance(kind, str)), \
#			type(kind)
#
#		if isinstance(kind, Kind):
#			self.__kind = kind
#		else: # if isinstance(kind, str):
#			STR_KIND_MAP \
#				= {
#					"null": Kind.Null,
#					"constant": Kind.Constant,
#					"type": Kind.Type,
#					"function": Kind.Function,
#					"procedure": Kind.Procedure,
#				}
#
#			assert (kind in STR_KIND_MAP), \
#				kind
#
#			self.__kind = STR_KIND_MAP[kind]
#
#
#		if (self.kind() == Kind.Null) or (self.kind() == Kind.Constant):
#			assert isinstance(typ, InstableTypeBase), \
#				type(typ)
#		elif self.kind() == Kind.Type:
#			assert (typ == None), \
#				type(typ)
#		elif self.kind() == Kind.Function:
#			assert isinstance(typ, DeclFunctionHeader), \
#				type(typ)
#		elif self.kind() == Kind.Procedure:
#			assert isinstance(typ, DeclProcedureHeader), \
#				typ(typ)
#		self.__typ = typ
#
#		self.__def_val = def_val
#
#		self._set_name(name)
#		#--------
#	#--------
#	def kind(self):
#		return self.__kind
#	def typ(self):
#		return self.__typ
#	def def_val(self):
#		return self.__def_val
#	def _set_name(self, n_name):
#		assert isinstance(n_name, str), \
#			type(n_name)
#		self.__name = name
#	def name(self):
#		return self.__name
#	#--------
#	def visit(self, visitor):
#		visitor.visitGeneric(self)
#	#--------
