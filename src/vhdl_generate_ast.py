#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_misc_ast import *

from enum import Enum, auto
#--------
# To make `isinstance(obj, GenerateStmt)` work
class GenerateStmt(Base):
	#--------
	def __init__(self, label, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
		self.__label = label
	def label(self):
		return self.__label
	def visit(self, visitor):
		visitor.visitGenerateStmt(self)
	#--------
class ForGenerateStmt(GenerateStmt):
	#--------
	def __init__(self, label, var_name, rang, body=[], *, src_loc_at=1):
		#--------
		super().__init__(label, src_loc_at=src_loc_at + 1)
		#--------
		self.__var_name = var_name
		self.__rang = rang
		self.__body = body
		#--------
	#--------
	def var_name(self):
		return self.__var_name
	def rang(self):
		return self.__rang
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitForGenerateStmt(self)
	#--------
class IfGenerateStmt(GenerateStmt):
	def __init__(self, label, nodes=[], *, src_loc_at=1):
		super().__init__(label, src_loc_at=src_loc_at + 1)
		self.__nodes = nodes
	def nodes(self):
		return self.__nodes
#--------
