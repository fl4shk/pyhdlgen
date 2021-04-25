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
	def __init__(self, generics={}, ports={}, *,
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
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitDeclComponent(self)
	#--------
#--------
class DeclEntity(Base):
	#--------
	def __init__(self, generics={}, ports={}, decls={}, archs={}, *,
		name="", src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		self.__generics = generics

		self.__ports = ports

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
	def __init__(self, decls={}, body_ul=[], body_l={}, *, name="",
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# Declarations
		self.__decls = decls

		# Unlabelled statements body
		self.__body_ul = body_ul

		# Labelled statements body
		self.__body_l = body_l

		self._set_name(name)
		#--------
	#--------
	def decls(self):
		return self.__decls
	def body_ul(self):
		return self.__body_ul
	def body_l(self):
		return self.__body_l
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	#--------
	def visit(self, visitor):
		visitor.visitDeclArchitecture(self)
	#--------
#--------
class Package(Base):
	pass
#--------
