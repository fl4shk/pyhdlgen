#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_misc_ast import *
from vhdl_misc_ast import *

from enum import Enum, auto
#--------
class DeclComponent(Base):
	#--------
	def __init__(self, generics=NamedObjList(), ports=NamedObjList(), *,
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
	def __init__(self, generics=NamedObjList(), ports=NamedObjList(),
		decls=NamedObjList(), archs=NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		super().__init__(name=name, src_loc_at=src_loc_at + 1)
		#--------
		self.__generics = generics

		self.__ports = ports

		# declarations
		self.__decls = decls

		# Architectures
		self.__archs = archs

		self._set_name(name)
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
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitDeclEntity(self)
	#--------
#--------
class DeclArch(Base):
	#--------
	def __init__(self, decls=NamedObjList(), body=[], *, name="",
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		# declarations
		self.__decls = decls

		# Unlabelled statements body
		self.__body = body

		self._set_name(name)
		#--------
	#--------
	def decls(self):
		return self.__decls
	def body(self):
		return self.__body
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitDeclArch(self)
	#--------
#--------
class DeclPackage(Base):
	#--------
	def __init__(self, generics=NamedObjList(), decls=NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__generics = generics
		self.__decls = decls
		self._set_name(name)
		#--------
	#--------
	def generics(self):
		return self.__generics
	def decls(self):
		return self.__decls
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitDeclPackage(self)
	#--------
class DeclPackageBody(Base):
	#--------
	def __init__(self, decls=NamedObjList(), *, name="", src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(decls, NamedObjList), \
			type(decls)
		self.__decls = decls
		self._set_name(name)
		#--------
	#--------
	def decls(self):
		return self.__decls
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name
	def name(self):
		return self.__name
	#--------
	def visit(self, visitor):
		visitor.visitDeclPackageBody(self)
	#--------
#--------
