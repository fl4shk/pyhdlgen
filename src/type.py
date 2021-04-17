#!/usr/bin/env python3

#--------
from misc_util import *
import misc_ast as ast
#--------
class Bit(ast.Base):
	def __init__(self, parent):
		super().__init__(parent)
	def visit(self, visitor):
		visitor.visitBit(self)

class StdLogic(ast.Base):
	def __init__(self, parent):
		super().__init__(parent)
	def visit(self, visitor):
		visitor.visitStdLogic(self)

class Boolean(ast.Base):
	def __init__(self, parent):
		super().__init__(parent)
	def visit(self, visitor):
		visitor.visitBoolean(self)

class Integer(ast.Base):
	def __init__(self, parent):
		super().__init__(parent)
	def visit(self, visitor):
		visitor.visitInteger(self)
class Natural(ast.Base):
	def __init__(self, parent):
		super().__init__(parent)
	def visit(self, visitor):
		visitor.visitNatural(self)
#--------
class VectorBase(ast.Base):
	def __init__(self, parent, rang):
		super().__init__(parent)

		# `rang` can be `None` in the case of an unconstrained vector
		self.__rang = rang
	def rang(self):
		return self.__rang
	def visit(self, visitor):
		visitor.visitVectorBase(self)

class BitVector(VectorBase):
	def __init__(self, parent, rang):
		super().__init__(parent, rang)
	def visit(self, visitor):
		visitor.visitBitVector(self)

class Slv(VectorBase):
	def __init__(self, parent, rang):
		super().__init__(parent, rang)
	def visit(self, visitor):
		visitor.visitSlv(self)
class Unsigned(VectorBase):
	def __init__(self, parent, rang):
		super().__init__(parent, rang)
	def visit(self, visitor):
		visitor.visitUnsigned(self)
class Signed(VectorBase):
	def __init__(self, parent, rang):
		super().__init__(parent, rang)
	def visit(self, visitor):
		visitor.visitSigned(self)

class BooleanVector(VectorBase):
	def __init__(self, parent, rang):
		super().__init__(parent, rang)
	def visit(self, visitor):
		visitor.visitBooleanVector(self)

class IntegerVector(VectorBase):
	def __init__(self, parent, rang):
		super().__init__(parent, rang)
	def visit(self, visitor):
		visitor.visitIntegerVector(self)
#class NaturalVector(VectorBase):
#	def __init__(self, parent, rang):
#		super().__init__(parent, rang)
#	def visit(self, visitor):
#		visitor.visitNaturalVector(self)

class DeclArray(VectorBase):
	def __init__(self, parent, rang, elem_t):
		super().__init__(parent, rang)

		# `elem_t` can be an existing type, a `DeclType`, a `DeclSubtype`,
		# or a `TypeGeneric`
		self.__elem_t = elem_t
	def elem_t(self):
		return self.__elem_t
	def visit(self, visitor):
		visitor.visitDeclArray(self)
#--------
class Range(ast.Base):
	#--------
	def __init__(self, parent, high, low=0, is_downto=False,
		is_natural=True):
		#--------
		super().__init__(parent)
		#--------
		self.__high = high
		self.__low = low
		self.__is_downto = is_downto
		self.__is_natural = is_natural
		#--------
	#--------
	def high(self):
		return self.__high
	def low(self):
		return self.__low
	def is_downto(self):
		return self.__is_downto
	def is_natural(self):
		return self.__is_natural
	#--------
	def visit(self, visitor):
		visitor.visitRange(self)
	#--------
#--------
