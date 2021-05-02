#!/usr/bin/env python3

#--------
from misc_util import *

#from vhdl_misc_ast import *
#from vhdl_expr_ast import *
#from vhdl_type_ast import *

import vhdl_ast.vhdl_ast as vhdl_ast

from enum import Enum, auto
#--------
#class Generic(vhdl_ast.Base, vhdl_ast.HasNameBase):
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
#		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
#		vhdl_ast.HasNameBase.__init__(self, name=name)
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
#			assert isinstance(typ, vhdl_ast.InstableTypeBase), \
#				type(typ)
#		elif self.kind() == Kind.Type:
#			assert (typ == None), \
#				type(typ)
#		elif self.kind() == Kind.Function:
#			assert isinstance(typ, vhdl_ast.Function), \
#				type(typ)
#		elif self.kind() == Kind.Procedure:
#			assert isinstance(typ, vhdl_ast.Procedure), \
#				typ(typ)
#		self.__typ = typ
#
#		self.__def_val = def_val
#		#--------
#	#--------
#	def kind(self):
#		return self.__kind
#	def typ(self):
#		return self.__typ
#	def def_val(self):
#		return self.__def_val
#	#--------
#	def visit(self, visitor):
#		visitor.visitGeneric(self)
#	#--------
