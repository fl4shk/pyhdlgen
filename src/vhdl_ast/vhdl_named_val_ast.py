#!/usr/bin/env python3

#--------
from misc_util import *

#from vhdl_ast.vhdl_misc_ast import *
#from vhdl_ast.vhdl_expr_ast import *
#from vhdl_ast.vhdl_type_ast import *

import vhdl_ast.vhdl_ast as vhdl_ast

from enum import Enum, auto
#--------
# Named values, such as ports and signals
class NamedValBase(vhdl_ast.Expr, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		#--------
		vhdl_ast.Expr.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(typ, vhdl_ast.InstableTypeBase), \
			type(typ)
		self.__typ = typ

		assert ((def_val is None) or isinstance(def_val, vhdl_ast.Expr)), \
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
	def left(self, inner=None):
		return vhdl_ast.AttrExprLeft(self, inner)
	def right(self, inner=None):
		return vhdl_ast.AttrExprRight(self, inner)

	def high(self, inner=None):
		return vhdl_ast.AttrExprHigh(self, inner)
	def low(self, inner=None):
		return vhdl_ast.AttrExprLow(self, inner)

	def length(self):
		return vhdl_ast.AttrExprLength(self)
	def __len__(self):
		return self.length()

	def ascending(self):
		return vhdl_ast.AttrExprAscending(self)
	#--------
	def event(self):
		return vhdl_ast.AttrExprEvent(self)
	def active(self):
		return vhdl_ast.AttrExprActive(self)
	def last_event(self):
		return vhdl_ast.AttrExprLastEvent(self)
	def last_value(self):
		return vhdl_ast.AttrExprLastValue(self)
	def last_active(self):
		return vhdl_ast.AttrExprLastActive(self)
	#--------
	def rising_edge(self):
		return vhdl_ast.RisingEdge(self)
	def falling_edge(self):
		return vhdl_ast.FallingEdge(self)
	#--------
	def rang(self):
		return vhdl_ast.AttrTypeRange(self)
	def reverse_rang(self):
		return vhdl_ast.AttrTypeReverseRange(self)
	#--------
#--------
class Signal(NamedValBase):
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
class Variable(NamedValBase):
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
class Constant(NamedValBase):
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
class GenericValBase(NamedValBase):
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
	def is_lvalue(self):
		return ((self.direction() == PortBase.Direction.Out)
			or (self.direction() == PortBase.Direction.Inout))
	#--------
class Port(PortBase):
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitPort(self)
class SigPort(PortBase):
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSigPort(self)
class VarPort(PortBase):
	def __init__(self, direction, typ, def_val=None, *, name="",
		src_loc_at=1):
		super().__init__(direction, typ, def_val, name=name,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitVarPort(self)
#--------
