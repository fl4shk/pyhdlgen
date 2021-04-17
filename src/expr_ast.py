#!/usr/bin/env python3

#--------
from misc_util import *
from misc_ast import *
#--------
class Expr(Base):
	#--------
	def __init__(self, val):
		super().__init__()

		self.__val = val
	#--------
	def val(self):
		return self.__val
	#--------
	def visit(self, visitor):
		visitor.visitExpr(self)
	#--------
	def __add__(self, other):
		return Add(self, other)
	def __sub__(self, other):
		return Sub(self, other)
	def __neg__(self):
		return Neg(self)

	def __mul__(self, other):
		return Mul(self, other)
	def __floordiv__(self, other):
		return Div(self, other)
	def __mod__(self, other):
		return Mod(self, other)

	def __rshift__(self, other):
		return Rshift(self, other)
	def __lshift__(self, other):
		return Lshift(self, other)

	def __and__(self, other):
		return And(self, other)
	def __or__(self, other):
		return Or(self, other)
	def __xor__(self, other):
		return Xor(self, other)
	def __invert__(self):
		return Not(self)

	def __lt__(self, other):
		return Lt(self, other)
	def __gt__(self, other):
		return Gt(self, other)
	def __le__(self, other):
		return Le(self, other)
	def __ge__(self, otehr):
		return Ge(self, other)
	def __eq__(self, other):
		return Eq(self, other)
	def __ne__(self, other):
		return Ne(self, other)
	#--------
#--------
class Const(Expr):
	#--------
	def __init__(self, val):
		#--------
		super().__init__(val)
		#--------
		# Force `self.__val` to be a `str`
		if isinstance(val, Const):
			self.__val = val.val()
		elif isinstance(val, str):
			self.__val = val
		else:
			self.__val = str(val)
		#--------
	#--------
	def val(self):
		return self.__val
	#--------
	def visit(self, visitor):
		visitor.visitConst(self)
	#--------
#--------
class BinopBase(Expr):
	#--------
	def __init__(self, left, right):
		super().__init__()

		self.__left = left
		self.__right = right
	#--------
	def left(self):
		return self.__left
	def right(self):
		return self.__right
	#--------
	def visit(self, visitor):
		visitor.visitBinopBase(self)
	#--------
#--------
