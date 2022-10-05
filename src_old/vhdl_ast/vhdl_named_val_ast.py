#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
# Named values, such as ports and signals
class NamedValBase(ast.Expr, ast.HasNameBase):
	#--------
	def __init__(self, typ, def_val=None, *, name="", src_loc_at=1):
		#--------
		ast.Expr.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(typ, ast.InstableTypeBase), \
			do_type_assert_psconcat(typ)
		self.__typ = typ

		assert ((def_val is None) or isinstance(def_val, ast.Expr)), \
			do_type_assert_psconcat(def_val)
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
		return ast.AttrExprLeft(self, inner)
	def right(self, inner=None):
		return ast.AttrExprRight(self, inner)

	def high(self, inner=None):
		return ast.AttrExprHigh(self, inner)
	def low(self, inner=None):
		return ast.AttrExprLow(self, inner)

	def length(self):
		return ast.AttrExprLength(self)
	def __len__(self):
		return self.length()

	def ascending(self):
		return ast.AttrExprAscending(self)
	#--------
	def event(self):
		return ast.AttrExprEvent(self)
	def active(self):
		return ast.AttrExprActive(self)
	def last_event(self):
		return ast.AttrExprLastEvent(self)
	def last_value(self):
		return ast.AttrExprLastValue(self)
	def last_active(self):
		return ast.AttrExprLastActive(self)
	#--------
	def rising_edge(self):
		return ast.RisingEdge(self)
	def falling_edge(self):
		return ast.FallingEdge(self)
	#--------
	def rang(self):
		return ast.AttrTypeRange(self)
	def reverse_rang(self):
		return ast.AttrTypeReverseRange(self)
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
			do_type_assert_psconcat(is_shared)
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
	def has_typical_direction(self):
		return ((self.direction() == PortBase.Direction.In)
			or (self.direction() == PortBase.Direction.Out)
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
