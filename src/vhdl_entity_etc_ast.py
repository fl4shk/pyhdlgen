#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_misc_ast import *
#from vhdl_generic_port_ast import *
from vhdl_misc_ast import *

from enum import Enum, auto
#--------
class DeclComponent(Base):
	#--------
	def __init__(self, generics=NamedObjDict(), ports=NamedObjDict(), *,
		name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		self.__generics = generics
		self.__ports = ports
		self._set_name(name)
		#--------
	#--------
	def generics(self):
		return self.__generics
	def ports(self):
		return self.__ports
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def n_name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitDeclComponent(self)
	#--------
#--------
class DeclEntity(DeclComponent):
	#--------
	def __init__(self, generics=NamedObjDict(), ports=NamedObjDict(),
		decls=NamedObjDict(), archs=NamedObjDict(), *, name="",
		src_loc_at=1):
		#--------
		super().__init__(generics, ports, name=name,
			src_loc_at=src_loc_at + 1)
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
	def __init__(self, decls=NamedObjDict(), stms_ul=[],
		stmts_l=NamedObjDict(), *, name="", src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# Declarations
		self.__decls = decls

		# Unlabelled statements
		self.__stms_ul = stms_ul

		# Labelled statements
		self.__stmts_l = stmts_l

		self._set_name(name)
		#--------
	#--------
	def decls(self):
		return self.__decls
	def stms_ul(self):
		return self.__stms_ul
	def stmts_l(self):
		return self.__stmts_l
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	#--------
	def visit(self, visitor):
		visitor.visitDeclArchitecture(self)
	#--------
#--------
