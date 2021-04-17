#!/usr/bin/env python3

#--------
from misc_util import *
#--------
class Base:
	def __init__(self, parent):
		self.__parent = parent
	def visit(self, visitor):
		visitor.visitBase(self)
#--------
# A comment
class Com(Base):
	def __init__(self, parent, val):
		super().__init__(parent)
		self.__val = val
	def val(self):
		return self.__val
	def visit(self, visitor):
		visitor.visitCom(self)
#--------
# type whatever_t is
class DeclType(Base):
	def __init__(self, parent, typ):
		super().__init__(parent)
		self.__typ = typ
	def typ(self):
		return self.__typ
	def visit(self, visitor):
		visitor.visitDeclType(self)

# subtype whatever_t is
class DeclSubtype(DeclType):
	def __init__(self, parent, typ, layout):
		super().__init__(parent, typ)

		# `layout` is expected to be a `list` where each element is a
		# `Range` (in the case of array/vector ranges) or a `dict` (in the
		# case of constraining an unconstrained record).
		self.__layout = layout
	def layout(self):
		return self.__layout
	def visit(self, visitor):
		visitor.visitDeclSubtype(self)
#--------
