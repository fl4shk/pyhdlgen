#!/usr/bin/env python3

#--------
from misc_util import *
from misc_ast import *
#--------
class Expr(Base):
	#--------
	def __init__(self):
		super().__init__()
	#--------
	def visit(self, visitor):
		visitor.visitExpr(self)
	#--------
	def eq(self, other):
		return Binop("assign", self, other)

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
class Const(Expr):
	#--------
	def __init__(self, val):
		#--------
		super().__init__()
		#--------
		assert hasattr(val, "__str__")
		self.__val = val
		#--------
	#--------
	def val(self):
		return self.__val
	#--------
	def visit(self, visitor):
		visitor.visitConst(self)
	#--------
	def __str__(self):
		return str(self.val())
	#--------
#--------
class Unop(Expr):
	#--------
	class Kind(enum.Enum):
		Abs = auto()
		Neg = auto()
		Not = auto()

		STR_KIND_MAP \
			= {
				"abs": Kind.Abs,
				"-": Kind.Neg,
				"~": Kind.Not,
			}
	#--------
	def __init__(self, kind, val):
		#--------
		super().__init__()
		#--------
		Kind = Unop.Kind

		assert (isinstance(kind, Kind) or isinstance(kind, str)), \
			str(type(kind))

		if isinstance(kind, Kind):
			self.__kind = kind
		else: # if isinstance(kind, str):
			self.__kind = Kind.STR_KIND_MAP[kind]
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
class Binop(Expr):
	#--------
	class Kind(enum.Enum):
		Assign = auto()

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

		STR_KIND_MAP \
			= {
				"assign": Kind.Assign,

				"+": Kind.Add.
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
				">": Kind,Gt,
				"<=": Kind.Le,
				">=": Kind.Ge,
				"==": Kind.Eq,
				"!=": Kind.Ne,
			}
	#--------
	def __init__(self, kind, left, right):
		#--------
		super().__init__()
		#--------
		Kind = Binop.Kind

		assert (isinstance(kind, Kind) or isinstance(kind, str)), \
			str(type(kind))

		if isinstance(kind, Kind):
			self.__kind = kind
		else: # if isinstance(kind, str):
			self.__kind = Kind.STR_KIND_MAP[kind]

		self.__left = left
		self.__right = right
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
		visitor.visitBinopBase(self)
	#--------
#--------
class PartSel(Expr):
	#--------
	def __init__(self, to_ps, ind_rang):
		#--------
		super().__init__()
		#--------
		# Object to part-select
		self.__to_ps = to_ps

		# Index or range
		self.__ind_rang = ind_rang
		#--------
	#--------
	def to_ps(self):
		return self.__to_ps
	def ind_rang(self):
		return self.__ind_rang
	#--------
	def visit(self, visitor):
		visitor.visitPartSel(self)
	#--------
#--------
class Cat(Expr):
	#--------
	def __init__(self, *args):
		super().__init__()
		self.__args = args
	#--------
	def args(self):
		return self.__args
	#--------
	def visit(self, visitor):
		visitor.visitCat(self)
	#--------
#--------
