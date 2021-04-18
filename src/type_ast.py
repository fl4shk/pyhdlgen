#!/usr/bin/env python3

#--------
from misc_util import *
from misc_ast import *
from expr_ast import *

from enum import Enum, auto
#--------
class Bit(Base):
	def __init__(self):
		super().__init__()
	def visit(self, visitor):
		visitor.visitBit(self)

class StdLogic(Base):
	def __init__(self):
		super().__init__()
	def visit(self, visitor):
		visitor.visitStdLogic(self)

class Boolean(Base):
	def __init__(self):
		super().__init__()
	def visit(self, visitor):
		visitor.visitBoolean(self)

class Integer(Base):
	def __init__(self):
		super().__init__()
	def visit(self, visitor):
		visitor.visitInteger(self)
class Natural(Base):
	def __init__(self):
		super().__init__()
	def visit(self, visitor):
		visitor.visitNatural(self)
#--------
class VectorBase(Base):
	def __init__(self, rang):
		super().__init__()

		# `rang` can be `None` in the case of an unconstrained vector
		self.__rang = rang
	def rang(self):
		return self.__rang
	def visit(self, visitor):
		visitor.visitVectorBase(self)

class BitVector(VectorBase):
	def __init__(self, rang):
		super().__init__(rang)
	def visit(self, visitor):
		visitor.visitBitVector(self)
class BitVectorR(BitVector):
	def __init__(self, width, low=0, is_downto=True):
		super().__init__(Range(width, low, is_downto))

class Slv(VectorBase):
	def __init__(self, rang):
		super().__init__(rang)
	def visit(self, visitor):
		visitor.visitSlv(self)
class SlvR(Slv):
	def __init__(self, width, low=0, is_downto=True):
		super().__init__(Range(width, low, is_downto))

class Unsigned(VectorBase):
	def __init__(self, rang):
		super().__init__(rang)
	def visit(self, visitor):
		visitor.visitUnsigned(self)
class UnsignedR(Unsigned):
	def __init__(self, width, low=0, is_downto=True):
		super().__init__(Range(width, low, is_downto))
	
class Signed(VectorBase):
	def __init__(self, rang):
		super().__init__(rang)
	def visit(self, visitor):
		visitor.visitSigned(self)
class SignedR(Signed):
	def __init__(self, width, low=0, is_downto=True):
		super().__init__(Range(width, low, is_downto))

class BooleanVector(VectorBase):
	def __init__(self, rang):
		super().__init__(rang)
	def visit(self, visitor):
		visitor.visitBooleanVector(self)
class BooleanVectorR(BooleanVector):
	def __init__(self, width, low=0, is_downto=True):
		super().__init__(Range(width, low, is_downto))

class IntegerVector(VectorBase):
	def __init__(self, rang):
		super().__init__(rang)
	def visit(self, visitor):
		visitor.visitIntegerVector(self)
class IntegerVectorR(IntegerVector):
	def __init__(self, width, low=0, is_downto=True):
		super().__init__(Range(width, low, is_downto))

class NaturalVector(VectorBase):
	def __init__(self, rang):
		super().__init__(rang)
	def visit(self, visitor):
		visitor.visitNaturalVector(self)
class NaturalVectorR(NaturalVector):
	def __init__(self, width, low=0, is_downto=True):
		super().__init__(Range(width, low, is_downto))

class Array(VectorBase):
	def __init__(self, rang, elem_t):
		super().__init__(rang)

		# `elem_t` can be a preexisting type, a `DeclType`, or a
		# `DeclSubtype`.
		self.__elem_t = elem_t
	def elem_t(self):
		return self.__elem_t
	def visit(self, visitor):
		visitor.visitArray(self)

class Range(Base):
	#--------
	def __init__(self, width, low=0, is_downto=True):
		#--------
		super().__init__()
		#--------
		Expr.assert_const(width)
		self.__width = Literal.cast_maybe(width)

		Expr.assert_const(low)
		self.__low = Literal.cast_maybe(low)

		self.__is_downto = is_downto
		#self.__is_natural = is_natural
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
	#def is_natural(self):
	#	return self.__is_natural
	#--------
	def visit(self, visitor):
		visitor.visitRange(self)
	#--------
class UnconstrRange(Base):
	def __init__(self, is_natural=True):
		super().__init__()
		self.__is_natural = is_natural
	def is_natural(self):
		return self.__is_natural
	def visit(self, visitor):
		visitor.visitUnconstrRange(self)
#--------
class Record(Base):
	#--------
	def __init__(self, layout):
		super().__init__()

		# `layout` is expected to be a `dict` mapping element names to
		# types, where types can be 
		self.__layout = layout
	#--------
	def layout(self):
		return self.__layout
	#--------
	def visit(self, visitor):
		visitor.visitRecord(self)
	#--------
#--------
