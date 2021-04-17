#!/usr/bin/env python3

#--------
from misc_util import *
from misc_ast import *
from type_ast import *
#--------
class Expr(Base):
	#--------
	def __init__(self):
		super().__init__()
	#--------
	def visit(self, visitor):
		visitor.visitExpr(self)
	#--------
	def is_lhs(self):
		return False
	#--------
	@staticmethod
	def is_const(other):
		return (isinstance(other, Const) 
			or isinstance(other, int) or hasattr(other, "__str__"))
	@staticmethod
	def check_const(other):
		assert Expr.is_const(other), \
			str(type(other))

	@staticmethod
	def is_valid(other):
		return (isinstance(other, Expr) or isinstance(other, int)
			or hasattr(other, "__str__"))
	@staticmethod
	def check_valid(other):
		assert Expr.is_valid(other), \
			str(type(other))
	#--------
	def eq(self, other):
		assert self.is_lhs()
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
		Expr.check_const(val)

		if isinstance(val, Expr):
			assert val.is_lhs()

		self.__val = val
		#--------
	#--------
	def val(self):
		return self.__val
	#--------
	def visit(self, visitor):
		visitor.visitConst(self)
	#--------
	def is_lhs(self):
		return True
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
				"abs": Unop.Kind.Abs,
				"-": Unop.Kind.Neg,
				"~": Unop.Kind.Not,
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

		Expr.check_valid(val)
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
		return self.val().is_lhs()
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
				"assign": Binop.Kind.Assign,

				"+": Binop.Kind.Add.
				"-": Binop.Kind.Sub,

				"*": Binop.Kind.Mul,
				"//": Binop.Kind.Div,
				"%": Binop.Kind.Mod,
				"rem": Binop.Kind.Rem,

				"**": Binop.Kind.Pow,

				"<<": Binop.Kind.Lshift,
				">>": Binop.Kind.Rshift,
				"rol": Binop.Kind.Rol,
				"ror": Binop.Kind.Ror,

				"&": Binop.Kind.And,
				"nand": Binop.Kind.Nand,
				"|": Binop.Kind.Or,
				"nor": Binop.Kind.Nor,
				"^": Binop.Kind.Xor,
				"xnor": Binop.Kind.Xnor,

				"<": Binop.Kind.Lt,
				">": Binop.Kind,Gt,
				"<=": Binop.Kind.Le,
				">=": Binop.Kind.Ge,
				"==": Binop.Kind.Eq,
				"!=": Binop.Kind.Ne,
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

		assert isinstance(left, Expr), \
			str(type(left))
		self.__left = left

		assert isinstance(right, Expr), \
			str(type(right))
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
		visitor.visitBinop(self)
	#--------
	def is_lhs(self):
		return (self.left().is_lhs() and self.right().is_lhs())
	#--------
#--------
class PartSel(Expr):
	#--------
	def __init__(self, val, ind_rang):
		#--------
		super().__init__()
		#--------
		#assert isinstance(val, Expr), \
		#	str(type(val))

		# Object to part-select
		Expr.check_valid(val)

		self.__val = val

		# Index or range
		assert (Expr.is_valid(ind_rang) or isinstance(ind_rang, Range)), \
			str(type(ind_rang))
		self.__ind_rang = ind_rang
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
	#--------
#--------
class Cat(Expr):
	#--------
	def __init__(self, *args):
		super().__init__()

		for arg in 
		self.__args = args
	#--------
	def args(self):
		return self.__args
	#--------
	def visit(self, visitor):
		visitor.visitCat(self)
	#--------
	def is_lhs(self):
		for arg in self.args():
			if arg.is_lhs
		return True
	#--------
#--------
