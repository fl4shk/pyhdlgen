#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
#class Generic(ast.Base, ast.HasNameBase):
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
#		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
#		ast.HasNameBase.__init__(self, name=name)
#		#--------
#		Kind = Generic.Kind
#		assert (isinstance(kind, Kind) or isinstance(kind, str)), \
#			do_type_assert_psconcat(kind)
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
#				do_type_assert_psconcat(kind)
#
#			self.__kind = STR_KIND_MAP[kind]
#
#
#		if (self.kind() == Kind.Null) or (self.kind() == Kind.Constant):
#			assert isinstance(typ, ast.InstableTypeBase), \
#				do_type_assert_psconcat(typ)
#		elif self.kind() == Kind.Type:
#			assert (typ == None), \
#				do_type_assert_psconcat(typ)
#		elif self.kind() == Kind.Function:
#			assert isinstance(typ, ast.Function), \
#				do_type_assert_psconcat(typ)
#		elif self.kind() == Kind.Procedure:
#			assert isinstance(typ, ast.Procedure), \
#				do_type_assert_psconcat(typ)
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
#--------
