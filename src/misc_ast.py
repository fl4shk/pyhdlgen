#!/usr/bin/env python3

#--------
from misc_util import *
from enum import Enum, auto
#--------
class Base:
	def __init__(self):
		pass
	def visit(self, visitor):
		visitor.visitBase(self)
#--------
# Comment
class Com(Base):
	def __init__(self, val):
		super().__init__()
		self.__val = val
	def val(self):
		return self.__val
	def visit(self, visitor):
		visitor.visitCom(self)
#--------
# type whatever_t is array(0 to 42) of asdf_t;
class DeclType(Base):
	def __init__(self, typ):
		super().__init__()
		self.__typ = typ
	def typ(self):
		return self.__typ
	def visit(self, visitor):
		visitor.visitDeclType(self)
# subtype whatever_t is unsigned(42 downto 0);
class DeclSubtype(DeclType):
	def __init__(self, typ, layout):
		super().__init__(typ)

		# `layout` is expected to be a `list` where each element is a
		# `Range` (in the case of array/vector ranges) or a `dict` (in the
		# case of constraining an unconstrained record).
		self.__layout = layout
	def layout(self):
		return self.__layout
	def visit(self, visitor):
		visitor.visitDeclSubtype(self)
#--------
class Entity(Base):
	#--------
	def __init__(self, generics=NameDict(), ports=NameDict(),
		decls=NameDict(), archs=NameDict()):
		#--------
		super().__init__()
		#--------
		self.__generics = generics
		self.__ports = ports
		self.__decls = decls
		self.__archs = archs
		#--------
	#--------
	def generics(self):
		return self.__generics
	def ports(self):
		return self.__ports
	def decls(self):
		return self.__decls
	def archs(self):
		return self.__archs
	#--------
	def __setattr__(self, name, key):
		self.decls()[name] = key
	def __getattr__(self, name):
		return self.decls()[name]
	#--------
	def visit(self, visitor):
		visitor.visitEntity(self)
	#--------
class Port(Base):
	#--------
	class Direction(enum.Enum):
		In = auto()
		Out = auto()
		Inout = auto()
	class Kind(enum.Enum):
		Null = auto()
		Sig = auto()
		Var = auto()
	#--------
	def __init__(self, kind, direction, typ, def_val=None):
		#--------
		super().__init__()
		#--------
		self.__kind = kind
		self.__direction = direction
		self.__typ = typ
		self.__def_val = def_val
		#--------
	#--------
	def kind(self):
		return self.__kind
	def direction(self):
		return self.__direction
	def typ(self):
		return self.__typ
	def def_val(self):
		return self.__def_val
	#--------
	def visit(self, visitor):
		visitor.visitPort(self)
	#--------
class Architecture(Base):
	#--------
	def __init__(self, 
	#--------
#--------
