#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_type_ast import *
from vhdl_behav_ast import *
#from vhdl_named_value_ast import *

from enum import Enum, auto
#--------
class Expr(Base):
	#--------
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	#--------
	def visit(self, visitor):
		visitor.visitExpr(self)
	#--------
	def is_lhs(self):
		return False

	@classmethod
	def is_literal(other):
		return (isinstance(other, Literal) or hasattr(other, "__str__"))
	@classmethod
	def assert_literal(other):
		assert Expr.is_literal(other), \
			type(other)

	def is_const(self):
		return False 
	def assert_const(self):
		assert self.is_const(), \
			type(self)

	# check to see if this is a valid `Expr` (or convertable to one)
	@classmethod
	def is_valid(other):
		return (isinstance(other, Expr) or isinstance(other, int)
			or hasattr(other, "__str__"))
	@classmethod
	def assert_valid(other):
		assert Expr.is_valid(other), \
			type(other)
	#--------
	def eq(self, other):
		#assert self.is_lhs()
		return AssignStmt(self, other)
		#return Binop("assign", self, other)

	def __getitem__(self, key):
		#if isinstance(key, slice):
		#	assert (key.step == None), \
		#		key.step
		return PartSel(self, key)

	def __abs__(self):
		return Unop("abs", self)
	def __add__(self, other):
		return Binop("+", self, other)
	def __sub__(self, other):
		return Binop("-", self, other)
	def __neg__(self):
		return Unop("-", self)

	def __mul__(self, other):
		return Binop("*", self, other)
	def __floordiv__(self, other):
		return Binop("//", self, other)
	def __mod__(self, other):
		return Binop("%", self, other)
	def rem(self, other):
		return Binop("rem", self, other)

	def __pow__(self, other):
		return Binop("**", self, other)

	def __lshift__(self, other):
		return Binop("<<", self, other)
	def __rshift__(self, other):
		return Binop(">>", self, other)
	def rol(self, other):
		return Binop("rol", self, other)
	def ror(self, other):
		return Binop("ror", self, other)

	def __and__(self, other):
		return Binop("&", self, other)
	def nand(self, other):
		return Binop("nand", self, other)
	def __or__(self, other):
		return Binop("|", self, other)
	def nor(self, other):
		return Binop("nor", self, other)
	def __xor__(self, other):
		return Binop("^", self, other)
	def xnor(self, other):
		return Binop("xnor", self, other)
	def __invert__(self):
		return Unop("~", self)

	def __lt__(self, other):
		return Binop("<", self, other)
	def __gt__(self, other):
		return Binop(">", self, other)
	def __le__(self, other):
		return Binop("<=", self, other)
	def __ge__(self, other):
		return Binop(">=", self, other)
	def __eq__(self, other):
		return Binop("==", self, other)
	def __ne__(self, other):
		return Binop("!=", self, other)
	#--------
#--------
class Literal(Expr):
	#--------
	def __init__(self, val, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		Expr.assert_literal(val)

		self.__val = val.val() \
			if isinstance(val, Literal) \
			else val
		#--------
	#--------
	def val(self):
		return self.__val
	#--------
	def visit(self, visitor):
		visitor.visitConst(self)
	#--------
	def is_lhs(self):
		return False
	def is_const(self):
		return True

	@classmethod
	def cast_maybe(other):
		return Literal(other) \
			if Expr.is_literal(other) \
			else other
	#--------
	def __str__(self):
		return str(self.val())
	#--------
# A VHDL literal character
class LitChar(Literal):
	def __init__(self, val, *, src_loc_at=1):
		assert hasattr(val, "__str__"), \
			type(val)
		super().__init__(str(val), src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitLitChar(self)
# A VHDL literal string
class LitStr(Literal):
	def __init__(self, val, *, src_loc_at=1):
		assert hasattr(val, "__str__"), \
			type(val)
		super().__init__(str(val), src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitLitStr(self)
#--------
class Unop(Expr):
	#--------
	class Kind(Enum):
		Abs = auto()
		Neg = auto()
		Not = auto()

	#--------
	def __init__(self, kind, val, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		Kind = Unop.Kind

		assert (isinstance(kind, Kind) or isinstance(kind, str)), \
			type(kind)

		if isinstance(kind, Kind):
			self.__kind = kind
		else: # if isinstance(kind, str):
			STR_KIND_MAP \
				= {
					"abs": Kind.Abs,
					"-": Kind.Neg,
					"~": Kind.Not,
				}

			assert (kind in STR_KIND_MAP), \
				kind
			self.__kind = STR_KIND_MAP[kind]

		Expr.assert_valid(val)
		self.__val = val
		#--------
	#--------
	def kind(self):
		return self.__kind
	def val(self):
		return self.__val
	#--------
	def visit(self, visitor):
		visitor.visitUnop(self)
	#--------
	def is_lhs(self):
		#return self.val().is_lhs()
		return False
	def is_const(self):
		return True
	#--------
class Binop(Expr):
	#--------
	class Kind(Enum):
		#Assign = auto()

		Add = auto()
		Sub = auto()

		Mul = auto()
		Div = auto()
		Mod = auto()
		Rem = auto()

		Pow = auto()

		Lshift = auto()
		Rshift = auto()
		Rol = auto()
		Ror = auto()

		And = auto()
		Nand = auto()
		Or = auto()
		Nor = auto()
		Xor = auto()
		Xnor = auto()

		Lt = auto()
		Gt = auto()
		Le = auto()
		Ge = auto()
		Eq = auto()
		Ne = auto()

	#--------
	def __init__(self, kind, left, right, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		Kind = Binop.Kind

		assert (isinstance(kind, Kind) or isinstance(kind, str)), \
			type(kind)

		if isinstance(kind, Kind):
			self.__kind = kind
		else: # if isinstance(kind, str):
			STR_KIND_MAP \
				= {
					#"assign": Kind.Assign,

					"+": Kind.Add,
					"-": Kind.Sub,

					"*": Kind.Mul,
					"//": Kind.Div,
					"%": Kind.Mod,
					"rem": Kind.Rem,

					"**": Kind.Pow,

					"<<": Kind.Lshift,
					">>": Kind.Rshift,
					"rol": Kind.Rol,
					"ror": Kind.Ror,

					"&": Kind.And,
					"nand": Kind.Nand,
					"|": Kind.Or,
					"nor": Kind.Nor,
					"^": Kind.Xor,
					"xnor": Kind.Xnor,

					"<": Kind.Lt,
					">": Kind.Gt,
					"<=": Kind.Le,
					">=": Kind.Ge,
					"==": Kind.Eq,
					"!=": Kind.Ne,
				}

			assert (kind in STR_KIND_MAP), \
				kind

			self.__kind = STR_KIND_MAP[kind]

		Expr.assert_valid(left)
		self.__left = Literal.cast_maybe(left)

		Expr.assert_valid(right)
		self.__right = Literal.cast_maybe(right)
		#--------
	#--------
	def kind(self):
		return self.__kind
	def left(self):
		return self.__left
	def right(self):
		return self.__right
	#--------
	def visit(self, visitor):
		visitor.visitBinop(self)
	#--------
	def is_lhs(self):
		#return (self.left().is_lhs() and self.right().is_lhs())
		return False
	def is_const(self):
		return True
	#--------
#--------
class PartSel(Expr):
	#--------
	def __init__(self, val, ind_rang, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# Object to part-select
		assert (isinstance(val, NamedValBase)
			or isinstance(val, PartSel)), \
			type(val)
		self.__val = val

		# Index, range, or slice
		assert (Expr.is_valid(ind_rang)
			or isinstance(ind_rang, ConRangeBase)
			or isinstance(ind_rang, slice)), \
			type(ind_rang)

		if not isinstance(ind_rang, slice):
			self.__ind_rang = Literal.cast_maybe(ind_rang)
		else: # isinstance(ind_rang, slice):
			# Convert the slice to a `Range`
			width = Literal.cast_maybe(ind_rang.stop) \
				- Literal.cast_maybe(ind_rang.start)

			low = Literal.cast_maybe(ind_rang.start)

			# This abuses the `step` field...
			cond_0 = ind_rang.step == None
			cond_1 = isinstance(ind_rang, str) \
				and ((ind_rang.step.lower() == "downto")
					or (ind_rang.step.lower() == "dt")
					or (ind_rang.step.lower() == "to"))
			assert cond_0 or cond_1, \
				ind_rang.step

			cond_2 = isinstance(ind_rang.step, str) \
				and ((ind_rang.step.lower() == "downto")
					or (ind_rang.step.lower() == "dt"))

			if (ind_rang.step == None) or cond_2:
				is_downto = True
			else: # if ind_rang.step.lower() == "to":
				is_downto = False

			self.__ind_rang = Range(width, low, is_downto)
		#--------
	#--------
	def val(self):
		return self.__val
	def ind_rang(self):
		return self.__ind_rang
	#--------
	def visit(self, visitor):
		visitor.visitPartSel(self)
	#--------
	def is_lhs(self):
		return self.val().is_lhs()
	def is_const(self):
		return self.val().is_const()
	#--------
#--------
class Cat(Expr):
	#--------
	def __init__(self, *args, src_loc_at=1):
		super().__init__()

		self.__args = []

		for arg in arg:
			Expr.assert_valid(arg)
			self.__args.append(Literal.cast_maybe(arg))
	#--------
	def args(self):
		return self.__args
	#--------
	def visit(self, visitor):
		visitor.visitCat(self)
	#--------
	def is_lhs(self):
		return False
	def is_const(self):
		return True
	#--------
#--------
