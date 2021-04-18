#!/usr/bin/env python3

#--------
from misc_util import *
from vhdl_misc_ast import *
from vhdl_generic_port_ast import *

from enum import Enum, auto
#--------
class DeclComponent(Base):
	#--------
	def __init__(self, name, generics=NameDict(), ports=NameDict(), *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__name = name
		self.__generics = generics
		self.__ports = ports
		#--------
	#--------
	def name(self):
		return self.__name
	def generics(self):
		return self.__generics
	def ports(self):
		return self.__ports
	#--------
	def visit(self, visitor):
		visitor.visitDeclComponent(self)
	#--------
#--------
class DeclEntity(DeclComponent):
	#--------
	def __init__(self, name, generics=NameDict(), ports=NameDict(),
		decls=NameDict(), archs=NameDict(), *, src_loc_at=1):
		#--------
		super().__init__(name, generics, ports, src_loc_at=src_loc_at + 1)
		#--------
		# Declarations
		self.__decls = decls

		# Architectures
		self.__archs = archs
		#--------
	#--------
	def decls(self):
		return self.__decls
	def archs(self):
		return self.__archs
	#--------
	def visit(self, visitor):
		visitor.visitDeclEntity(self)
	#--------
#--------
class DeclArchitecture(Base):
	#--------
	def __init__(self, name, decls=NameDict(), stms_ul=[],
		stmts_l=NameDict(), *, src_loc_at=1):
		#--------
		super().__init__(name, src_loc_at=src_loc_at + 1)
		#--------
		# Declarations
		self.__decls = decls

		# Unlabelled statements
		self.__stms_ul = stms_ul

		# Labelled statements
		self.__stmts_l = stmts_l
		#--------
	#--------
	def decls(self):
		return self.__decls
	def stms_ul(self):
		return self.__stms_ul
	def stmts_l(self):
		return self.__stmts_l
	#--------
	def visit(self, visitor):
		visitor.visitDeclArchitecture(self)
	#--------
#--------
#--------
