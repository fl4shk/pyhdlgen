#!/usr/bin/env python3

#--------
from misc_util import *
import vhdl_misc_ast as misc_ast
import vhdl_expr_ast as expr_ast
#from vhdl_expr_ast import BasicLiteral

from enum import Enum, auto
#--------
# To make `isinstance(obj, TypeBase)` work
class TypeBase(misc_ast.Base):
	#--------
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitTypeBase(self)
	#--------
	## Whether or not we can instantiate a `NamedValBase` of this type
	#def is_instable(self):
	#	return False
	#def is_unconstrained(self):
	#	return False
	#--------
#--------
# Base class for a type that can be instantiated directly (i.e. not a
# `Record` or `Array`)
class InstableTypeBase(TypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitInstableTypeBase(self)
#--------
# For `isinstance(obj, NamedTypeBase)`
class NamedTypeBase(InstableTypeBase):
	#--------
	def __init__(self, *, name="", src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
		self._set_name(name)
	#--------
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitNamedTypeBase(self)
	#--------
	## Create a `Qualified` expression
	#def qual_expr(self, expr):
	#	return Qualified(self, expr)

	## Create a `Cast` expression
	#def cast_expr(self, expr):
	#	return Cast(self, expr)
	#--------

# `type whatever_t is array(0 to 42) of asdf_t;`
class DeclType(NamedTypeBase):
	#--------
	def __init__(self, typ, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert (isinstance(typ, Array) or isinstance(typ, Record)
			or isinstance(typ, Range)), \
			type(typ)
		self.__typ = typ
		#--------
	#--------
	def typ(self):
		return self.__typ
	#--------
	def visit(self, visitor):
		visitor.visitDeclType(self)
	#--------
# `subtype whatever_t is unsigned(42 downto 0);`
class DeclSubtype(NamedTypeBase):
	#--------
	def __init__(self, typ, layout, *, name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(typ, TypeBase) \
			and (not isinstance(typ, DeclSubtype)), \
			type(typ)
		#assert typ.is_unconstrained(), \
		#	type(typ)
		self.__typ = typ

		assert isinstance(layout, list), \
			type(layout)
		self.__layout = layout
		#--------
	#--------
	def typ(self):
		return self.__typ
	def layout(self):
		return self.__layout
	#--------
	def visit(self, visitor):
		visitor.visitDeclDeclSubtype(self)
	#--------
#--------
class Bit(InstableTypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBit(self)

class StdLogic(InstableTypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitStdLogic(self)

class Boolean(InstableTypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBoolean(self)

class Integer(InstableTypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitInteger(self)
class Natural(InstableTypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitNatural(self)
#--------
class VectorBase(InstableTypeBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		# `rang` can be `None` in the case of an unconstrained vector
		self.__rang = rang
	def rang(self):
		return self.__rang
	def visit(self, visitor):
		visitor.visitVectorBase(self)

class BitVector(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBitVector(self)
class BitVectorR(BitVector):
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(high, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
class BitVectorW(BitVector):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)

class Slv(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSlv(self)
class SlvR(Slv):
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(high, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
class SlvW(Slv):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)

class Unsigned(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitUnsigned(self)
class UnsignedR(Unsigned):
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(high, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
class UnsignedW(Unsigned):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
	
class Signed(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSigned(self)
class SignedR(Signed):
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(high, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
class SignedW(Signed):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)

class BooleanVector(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBooleanVector(self)
class BooleanVectorR(BooleanVector):
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(high, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
class BooleanVectorW(BooleanVector):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)

class IntegerVector(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitIntegerVector(self)
class IntegerVectorR(IntegerVector):
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(high, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
class IntegerVectorW(IntegerVector):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)

class NaturalVector(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitNaturalVector(self)
class NaturalVectorR(NaturalVector):
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(high, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)
class NaturalVectorW(NaturalVector):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, low, is_downto),
			src_loc_at=src_loc_at + 1,
		)

class Array(TypeBase):
	#--------
	def __init__(self, rang, ElemT, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__rang = rang

		# `ElemT` can be a preexisting type, a `DeclType`, or a
		# `DeclSubtype`.
		self.__ElemT = ElemT
		#--------
	#--------
	def rang(self):
		return self.__rang
	def ElemT(self):
		return self.__ElemT
	#--------
	def visit(self, visitor):
		visitor.visitArray(self)
	#--------
class ArrayS(Array):
	def __init__(self, size, ElemT, is_downto=False, *,
		src_loc_at=1):
		super().__init__ \
		(
			rang=RangeW(width, 0, is_downto),
			ElemT=ElemT,
			src_loc_at=src_loc_at + 1
		)
class Record(TypeBase):
	#--------
	def __init__(self, layout, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		# `layout` is expected to be a `dict` mapping element names to
		# types
		assert isinstance(layout, dict), \
			type(layout)
		#for key in layout.keys()
		self.__layout = layout
	#--------
	def layout(self):
		return self.__layout
	#--------
	def visit(self, visitor):
		visitor.visitRecord(self)
	#--------
	#def is_unconstrained(self):
	#	pass
	#--------

# Base class for a constrained range, used for 
# `isinstance(obj, ConRangeBase)`
class ConRangeBase(TypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitConRangeBase(self)
	
class Range(ConRangeBase):
	#--------
	def __init__(self, high, low=0, is_downto=True, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__high = expr_ast.BasicLiteral.cast_opt(high)
		self.high().assert_const()

		self.__low = expr_ast.BasicLiteral.cast_opt(low)
		self.low().assert_const(low)

		self.__is_downto = is_downto
		#--------
	#--------
	def width(self):
		# width = high + 1 - low
		return ((self.high() + 1) - self.low())
	def high(self):
		# high = (width - 1) + low
		#return (self.low() + (self.width() - 1))
		return self.__high
	def low(self):
		return self.__low
	def is_downto(self):
		return self.__is_downto
	#--------
	def visit(self, visitor):
		visitor.visitRange(self)
	#--------
class RangeW(Range):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			high=expr_ast.BasicLiteral.cast_opt(width) - 1,
			low=low,
			is_downto=is_downto,
			src_loc_at=src_loc_at + 1,
		)
# `mynamedval'range` or `mytype'range`
class TickRange(ConRangeBase):
	def __init__(self, obj, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		# This isn't a perfect check since `DeclType` might be
		# unconstrained
		assert (isinstance(obj, NamedValBase) 
			or isinstance(obj, NamedTypeBase)), \
			type(obj)
		self.__obj = obj
	def obj(self):
		return self.__obj
	def visit(self, visitor):
		visitor.visitTickRange(self)

# An unconstrained range, such as `natural range <>`
class UnconRange(misc_ast.Base):
	def __init__(self, is_natural=True, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
		self.__is_natural = is_natural
	def is_natural(self):
		return self.__is_natural
	def visit(self, visitor):
		visitor.visitUnconRange(self)
#--------
