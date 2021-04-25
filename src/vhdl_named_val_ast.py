#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_named_obj_ast import *
from vhdl_expr_ast import *
from vhdl_type_ast import *

from enum import Enum, auto
#--------
# Named values, such as ports and signals
class NamedValBase(Expr):
	#--------
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(typ, InstableTypeBase), \
			type(typ)
		self.__typ = typ

		assert ((def_val is None) or isinstance(def_val, Expr)), \
			type(def_val)
		self.__def_val = def_val

		self._set_name(name)
		#--------
	#--------
	def typ(self):
		return self.__typ
	def def_val(self):
		return self.__def_val
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitNamedValBase(self)
	#--------
#--------
class Signal(NamedValBase):
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name, 
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSignal(self)
class Variable(NamedValBase):
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name, 
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSignal(self)
class Constant(NamedValBase):
	def __init__(self, typ, def_val, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitConstant(self)
#--------
class GenericValBase(NamedValBase):
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitGenericValBase(self)
# Not a `constant` generic, but basically equivalent to one
class RegularGeneric(GenericValBase):
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitRegularGeneric(self)
# A `constant` generic
class ConstantGeneric(GenericValBase):
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitConstantGeneric(self)
#--------
class PortBase(NamedValBase):
	#--------
	class Direction(Enum):
		In = auto()
		Out = auto()
		Inout = auto()
	#--------
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		#--------
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
		#--------
		Direction = PortBase.Direction

		STR_DIRECTION_MAP \
			= {
				"in": Direction.In,
				"out": Direction.Out,
				"inout": Direction.Inout,
			}

		self.__direction = convert_str_to_enum_opt(direction, Direction,
			STR_DIRECTION_MAP)
		#--------
	#--------
	def direction(self):
		return self.__direction
	#--------
	def visit(self, visitor):
		visitor.visitPortBase(self)
	#--------
class Port(PortBase)
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitPort(self)
class SigPort(PortBase)
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSigPort(self)
class VarPort(PortBase)
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitVarPort(self)
#--------
