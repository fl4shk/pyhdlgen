#!/usr/bin/env python3

#--------
from misc_util import *
from misc_ast import *
from expr_ast import *

from enum import Enum, auto
#--------
class TypeBase(Base):
	#--------
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitTypeBase(self)
	#--------
	## Whether or not we can instantiate a `NamedValue` of this type
	#def is_instable(self):
	#	return False
	#def is_unconstrained(self):
	#	return False
	##--------
#--------
# type whatever_t is array(0 to 42) of asdf_t;
class DeclType(TypeBase):
	#--------
	def __init__(self, typ, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
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
# subtype whatever_t is unsigned(42 downto 0);
class DeclSubtype(TypeBase):
	#--------
	def __init__(self, typ, layout, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(typ, TypeBase), \
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
		visitor.visitDeclSubtype(self)
	#--------
#--------
class Bit(TypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBit(self)

class StdLogic(TypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitStdLogic(self)

class Boolean(TypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBoolean(self)

class Integer(TypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitInteger(self)
class Natural(TypeBase):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitNatural(self)
#--------
class VectorBase(TypeBase):
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
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
			src_loc_at=src_loc_at + 1,
		)

class Slv(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSlv(self)
class SlvR(Slv):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
			src_loc_at=src_loc_at + 1,
		)

class Unsigned(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitUnsigned(self)
class UnsignedR(Unsigned):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
			src_loc_at=src_loc_at + 1,
		)
	
class Signed(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSigned(self)
class SignedR(Signed):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
			src_loc_at=src_loc_at + 1,
		)

class BooleanVector(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitBooleanVector(self)
class BooleanVectorR(BooleanVector):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
			src_loc_at=src_loc_at + 1,
		)

class IntegerVector(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitIntegerVector(self)
class IntegerVectorR(IntegerVector):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
			src_loc_at=src_loc_at + 1,
		)

class NaturalVector(VectorBase):
	def __init__(self, rang, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitNaturalVector(self)
class NaturalVectorR(NaturalVector):
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		super().__init__ \
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
			src_loc_at=src_loc_at + 1,
		)

class Array(VectorBase):
	def __init__(self, rang, ElemT, *, src_loc_at=1):
		super().__init__(rang, src_loc_at=src_loc_at + 1)

		# `ElemT` can be a preexisting type, a `DeclType`, or a
		# `DeclSubtype`.
		self.__ElemT = ElemT
	def ElemT(self):
		return self.__ElemT
	def visit(self, visitor):
		visitor.visitArray(self)
class ArrayR(Array):
	def __init__(self, width, ElemT, low=0, is_downto=False, *,
		src_loc_at=1):
		super().__init__
		(
			rang=Range(width, low, is_downto, src_loc_at=src_loc_at),
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
		for key in layout.keys()
		self.__layout = layout
	#--------
	def layout(self):
		return self.__layout
	#--------
	def visit(self, visitor):
		visitor.visitRecord(self)
	#--------

class Range(TypeBase):
	#--------
	def __init__(self, width, low=0, is_downto=True, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		Expr.assert_const(width)
		self.__width = Literal.cast_maybe(width)

		Expr.assert_const(low)
		self.__low = Literal.cast_maybe(low)

		self.__is_downto = is_downto
		#--------
	#--------
	def width(self):
		return
	def high(self):
		return (self.low() + (self.width() - Literal(1)))
	def low(self):
		return self.__low
	def is_downto(self):
		return self.__is_downto
	#--------
	def visit(self, visitor):
		visitor.visitRange(self)
	#--------
# An unconstrained range
class UnconRange(Base):
	def __init__(self, is_natural=True, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
		self.__is_natural = is_natural
	def is_natural(self):
		return self.__is_natural
	def visit(self, visitor):
		visitor.visitUnconRange(self)
#--------
