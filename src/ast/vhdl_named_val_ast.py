#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_expr_ast import *
from vhdl_type_ast import *

from enum import Enum, auto
#--------
# Named values, such as ports and signals
class _NamedValBase(_Expr, HasNameBase):
	#--------
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		#--------
		_Expr.__init__(self, src_loc_at=src_loc_at + 1)
		HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(typ, _InstableTypeBase), \
			type(typ)
		self.__typ = typ

		assert ((def_val is None) or isinstance(def_val, _Expr)), \
			type(def_val)
		self.__def_val = def_val
		#--------
	#--------
	def typ(self):
		return self.__typ
	def def_val(self):
		return self.__def_val
	#--------
	def visit(self, visitor):
		visitor.visitNamedValBase(self)
	#--------
#--------
class Signal(_NamedValBase):
	#--------
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name, 
			src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitSignal(self)
	#--------
	def is_lvalue(self):
		return True
	#--------
class Variable(_NamedValBase):
	#--------
	def __init__(self, typ, def_val=None, is_shared=False, *, name="",
		src_loc_at=1):
		super().__init__(typ, def_val, name=name, 
			src_loc_at=src_loc_at + 1)

		assert isinstance(is_shared, bool), \
			type(is_shared)
		self.__is_shared = is_shared
	#--------
	def is_shared(self):
		return self.__is_shared
	#--------
	def visit(self, visitor):
		visitor.visitSignal(self)
	#--------
	def is_lvalue(self):
		return True
	#--------
class Constant(_NamedValBase):
	#--------
	def __init__(self, typ, def_val, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitConstant(self)
	#--------
	def is_const(self):
		return True
	#--------
#--------
class _GenericValBase(_NamedValBase):
	#--------
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitGenericValBase(self)
	#--------
	def is_const(self):
		return True
	#--------
# Not a `constant` generic, but basically equivalent to one
class RegularGeneric(_GenericValBase):
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitRegularGeneric(self)
# A `constant` generic
class ConstantGeneric(_GenericValBase):
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		super().__init__(typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitConstantGeneric(self)
#--------
class _PortBase(_NamedValBase):
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
		Direction = _PortBase.Direction

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
	def is_lvalue(self):
		return ((self.direction() == _PortBase.Direction.Out)
			or (self.direction() == _PortBase.Direction.Inout))
	#--------
class Port(_PortBase)
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitPort(self)
class SigPort(_PortBase)
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSigPort(self)
class VarPort(_PortBase)
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitVarPort(self)
#--------
