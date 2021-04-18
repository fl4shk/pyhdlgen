#!/usr/bin/env python3

#--------
from misc_util import *
from misc_ast import *

from enum import Enum, auto
#--------
class Generic(Base):
	#--------
	class Kind(Enum):
		Null = auto()
		Constant = auto()
		Type = auto()
		Function = auto()
		Procedure = auto()
	#--------
	def __init__(self, kind, typ, def_val=None, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(kind, Generic.Kind), \
			type(kind)
		self.__kind = kind

		self.__typ = typ
		self.__def_val = def_val
		#--------
	#--------
	def kind(self):
		return self.__kind
	def typ(self):
		return self.__typ
	def def_val(self):
		return self.__def_val
	#--------
	def visit(self, visitor):
		visitor.visitGeneric(self)
	#--------
class Port(Base):
	#--------
	class Kind(Enum):
		Null = auto()
		Signal = auto()
		Variable = auto()
	class Direction(Enum):
		In = auto()
		Out = auto()
		Inout = auto()
	#--------
	def __init__(self, kind, direction, typ, def_val=None, *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(kind, Port.Kind), \
			type(kind)
		self.__kind = kind

		assert isinstance(direction, Port.Direction), \
			type(direction)
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
#--------
