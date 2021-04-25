#!/usr/bin/env python3

#--------
from misc_util import *

from vhdl_misc_ast import *
from vhdl_generic_port_map_ast import *

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
	def is_lvalue(self):
		return False
	def assert_lvalue(self):
		assert self.is_lvalue(), \
			type(self)
	def is_const(self):
		return False 
	def assert_const(self):
		assert self.is_const(), \
			type(self)

	@classmethod
	def is_basic_literal(other):
		return (isinstance(other, BasicLiteral) or isinstance(other, int)
			or isinstance(other, str))
	@classmethod
	def assert_basic_literal(other):
		assert Expr.is_basic_literal(other), \
			type(other)

	@classmethod
	def is_literal(other):
		return (Expr.is_basic_literal(other) \
			or (hasattr(other, "_is_literal_cstm")
				and other._is_literal_cstm()))
	@classmethod
	def assert_literal(other):
		assert Expr.is_literal(other), \
			type(other)

	# check to see if this is a valid `Expr` (or convertable to one)
	@classmethod
	def is_valid(other):
		# floats not supported yet!
		return (isinstance(other, Expr) or isinstance(other, int)
			or isinstance(other, str))
	@classmethod
	def assert_valid(other):
		assert Expr.is_valid(other), \
			type(other)
	#--------
	def eq(self, other):
		return AssignStmt(self, other)
	def seleq(self, expr, sel_waves):
		return SelAssignStmt(expr, self, sel_waves)

	def concur_eq(self, other, *, name=""):
		return ConcurAssignStmt(self, other, name="")
	def concur_seleq(self, expr, sel_waves, *, name=""):
		return ConcurSelAssignStmt(expr, self, sel_waves, name=name)

	def __getitem__(self, key):
		return PartSel(self, key)
	def __getattr__(self, key):
		return MembSel(self, key)

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
	def __radd__(self, other):
		return Binop("+", other, self)
	def __rsub__(self, other):
		return Binop("-", other, self)

	def __rmul__(self, other):
		return Binop("*", other, self)
	def __rfloordiv__(self, other):
		return Binop("//", other, self)
	def __rmod__(self, other):
		return Binop("%", other, self)
	def rrem(self, other):
		return Binop("rem", other, self)

	def __rpow__(self, other):
		return Binop("**", other, self)

	def __rlshift__(self, other):
		return Binop("<<", other, self)
	def __rrshift__(self, other):
		return Binop(">>", other, self)
	def rrol(self, other):
		return Binop("rol", other, self)
	def rror(self, other):
		return Binop("ror", other, self)

	def __rand__(self, other):
		return Binop("&", other, self)
	def rnand(self, other):
		return Binop("nand", other, self)
	def __ror__(self, other):
		return Binop("|", other, self)
	def rnor(self, other):
		return Binop("nor", other, self)
	def __rxor__(self, other):
		return Binop("^", other, self)
	def rxnor(self, other):
		return Binop("xnor", other, self)
	#--------
#--------
class BasicLiteral(Expr):
	#--------
	class Kind(Enum):
		Int = auto()
		Char = auto()
		Str = auto()
	class NumBase(Enum):
		Bin = auto()
		Oct = auto()
		Dec = auto()
		Hex = auto()
	#--------
	def __init__(self, kind, val, num_base="bin", *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		Kind = BasicLiteral.Kind

		STR_KIND_MAP \
			= {
				"int": Kind.Int,
				"char": Kind.Char,
				"str": Kind.Str,
			}

		self.__kind = convert_str_to_enum_opt(kind, Kind, STR_KIND_MAP)
		#--------
		Expr.assert_basic_literal(val)
		self.__val = val.val() \
			if isinstance(val, BasicLiteral) \
			else val
		#--------
		NumBase = BasicLiteral.NumBase

		STR_NUM_BASE_MAP \
			= {
				"bin": NumBase.Bin,
				"oct": NumBase.Oct,
				"dec": NumBase.Dec,
				"hex": NumBase.Hex,
			}

		self.__num_base = convert_str_to_enum_opt(num_base, NumBase,
			STR_NUM_BASE_MAP)
		#--------
	#--------
	def kind(self):
		return self.__kind
	def val(self):
		return self.__val
	def num_base(self):
		return self.__num_base
	#--------
	def visit(self, visitor):
		visitor.visitLiteral(self)
	#--------
	def is_const(self):
		return True

	@staticmethod
	def cast_opt(other):
		if Expr.is_basic_literal(other):
			if isinstance(other, BasicLiteral):
				return other
			elif isinstance(other, int):
				return BasicLiteral("int", other)
			else: # if isinstance(other, str):
				# This is a heuristic that should work for the common case
				# of writing VHDL.  It is still possible to make a
				# single-character string, but it has to be done manually
				# by creating an instance of the `StrLiteral` class.
				# Unlike VHDL, Python doesn't have a separation between
				# strings and single characters.
				return BasicLiteral("char", other) \
					if len(other) == 1 \
					else BasicLiteral("str", other)
		else: # if not Expr.is_basic_literal(other):
			return other
	#--------
class IntLiteral(BasicLiteral):
	def __init__(self, val, base="dec", *, src_loc_at=1):
		super().__init__("int", val, base, src_loc_at=src_loc_at + 1)
class CharLiteral(BasicLiteral):
	def __init__(self, val, base="bin", *, src_loc_at=1):
		super().__init__("char", val, base, src_loc_at=src_loc_at + 1)
class StrLiteral(BasicLiteral):
	def __init__(self, val, base="bin", *, src_loc_at=1):
		super().__init__("str", val, base, src_loc_at=src_loc_at + 1)
#--------
# Untyped (if not `Qualified`) aggregate:  (0 => '1', others => '0')
class Agg(Expr):
	#--------
	def __init__(self, layout, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(layout, dict), \
			type(layout)

		for key in layout:
			assert Expr.is_valid(layout[key]), \
				psconcat("{}: {}; type(val): {}".format(key, layout[key],
					type(layout[key])))
		self.__layout = layout
		#--------
	#--------
	def layout(self):
		return self.__layout
	#--------
	def visit(self, visitor):
		visitor.visitAgg(self)
	#--------
	def _is_literal_cstm(self):
		for key in self.layout():
			if not Expr.is_literal(self.layout()[key]):
				return False
		return True
	#--------
	def is_const(self):
		for key in self.layout():
			val = self.layout()[key]
			if not (Expr.is_literal(val)
				or (isinstance(val, Expr) and val.is_const())):
				return False
		return True
	#--------

# Example:  my_record_t'(my_natural => 0, my_slv => (others => '0'))
class Qualified(Expr):
	#--------
	def __init__(self, typ, expr, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(typ, InstableTypeBase), \
			type(typ)
		self.__typ = typ

		Expr.assert_valid(expr)
		self.__expr = BasicLiteral.cast_opt(expr)
		#--------
	#--------
	def typ(self):
		return self.__typ
	def expr(self):
		return self.__expr
	#--------
	def visit(self, visitor):
		visitor.visitQualified(self)
	#--------
	def is_const(self):
		return self.expr().is_const()
	#--------
# unsigned(my_slv)
class Cast(Expr):
	#--------
	def __init__(self, typ, expr, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__typ = typ
		self.__expr = expr
		#--------
	#--------
	def typ(self):
		return self.__typ
	def expr(self):
		return self.__expr
	#--------
	def visit(self, visitor):
		visitor.visitCast(self)
	#--------

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

		STR_KIND_MAP \
			= {
				"abs": Kind.Abs,
				"-": Kind.Neg,
				"~": Kind.Not,
			}

		self.__kind = convert_str_to_enum_opt(kind, Kind, STR_KIND_MAP)

		Expr.assert_valid(val)
		self.__val = BasicLiteral.cast_opt(val)
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
	def is_const(self):
		return self.val().is_const()
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

		STR_KIND_MAP \
			= {
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
		self.__kind = convert_str_to_enum_opt(kind, Kind, STR_KIND_MAP)

		Expr.assert_valid(left)
		self.__left = BasicLiteral.cast_opt(left)

		Expr.assert_valid(right)
		self.__right = BasicLiteral.cast_opt(right)
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
	def is_const(self):
		return (self.left().is_const() or self.right().is_const())
	#--------
#--------
# A part select:  `a[b]`
class PartSel(Expr):
	#--------
	def __init__(self, val, ind_rang, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# Object to part-select
		assert (isinstance(val, NamedValBase) or isinstance(val, PartSel)
			or isinstance(val, MembSel)), \
			type(val)
		self.__val = val

		# Index, range, or slice
		assert (Expr.is_valid(ind_rang)
			or isinstance(ind_rang, Range)
			or isinstance(ind_rang, slice)), \
			type(ind_rang)

		if not isinstance(ind_rang, slice):
			self.__ind_rang = BasicLiteral.cast_opt(ind_rang)
		else: # isinstance(ind_rang, slice):
			# Convert the slice to a `Range`
			#width = BasicLiteral.cast_opt(ind_rang.stop) \
			#	- BasicLiteral.cast_opt(ind_rang.start)
			high = BasicLiteral.cast_opt(ind_rang.stop) - 1

			low = BasicLiteral.cast_opt(ind_rang.start)

			# This abuses the `step` field...
			cond_0 = ind_rang.step == None
			cond_1 = isinstance(ind_rang, int) \
				and ((ind_rang.step == 1) or (ind_rang.step == -1))
			assert cond_0 or cond_1, \
				ind_rang.step

			cond_2 = isinstance(ind_rang.step, int) \
				and (ind_rang.step == -1)

			if (ind_rang.step == None) or cond_2:
				is_downto = True
			else: # if ind_rang.step == 1:
				is_downto = False

			self.__ind_rang = Range(high, low, is_downto)
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
	def is_lvalue(self):
		return self.val().is_lvalue()
	def is_const(self):
		return self.val().is_const()
	#--------
# A member select:  `a.b`
class MembSel(Expr):
	#--------
	def __init__(self, val, name, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert (isinstance(val, NamedValBase) or isinstance(val, PartSel)
			or isinstance(val, MembSel)), \
			type(val)
		self.__val = val

		assert isinstance(name, str), \
			type(name)
		self.__name = name
		#--------
	#--------
	def val(self):
		return self.__val
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitMembSel(self)
	#--------
#--------
# Concatenation:  `a & b & ...`
class Cat(Expr):
	#--------
	def __init__(self, *args, src_loc_at=1):
		super().__init__()

		self.__args = []

		for arg in arg:
			Expr.assert_valid(arg)
			self.__args.append(BasicLiteral.cast_opt(arg))
	#--------
	def args(self):
		return self.__args
	#--------
	def visit(self, visitor):
		visitor.visitCat(self)
	#--------
	def is_const(self):
		for arg in self.args():
			if not arg.is_const():
				return False
		return True
	#--------
#--------
# Function call
class FunctionCall(Expr):
	#--------
	def __init__(self, function, assoc_list, *, src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		self.__function = function

		#assert (assoc_list is None or isinstance(assoc_list, list)
		#	or isinstance(assoc_list, dict)), \
		#	type(assoc_list)
		assert isinstance(assoc_list, AssocList), \
			type(assoc_list)
		self.__assoc_list = assoc_list
		#--------
	#--------
	def function(self):
		return self.__function
	def assoc_list(self):
		return self.__assoc_list
	#--------
	def visit(self, visitor):
		visitor.visitFunctionCall(self)
	#--------
#--------
