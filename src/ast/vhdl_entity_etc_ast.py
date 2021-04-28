#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_misc_ast import *
from vhdl_misc_ast import *

from enum import Enum, auto
#--------
class Component(Base, HasNameBase):
	#--------
	def __init__(self, generics=NamedObjList(), ports=NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		Base.__init__(self, src_loc_at=src_loc_at + 1)
		HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(ports, NamedObjList), \
			type(ports)
		self.__ports = ports
		#--------
	#--------
	def generics(self):
		return self.__generics
	def ports(self):
		return self.__ports
	#--------
	def visit(self, visitor):
		visitor.visitComponent(self)
	#--------
#--------
class Entity(Base, HasNameBase):
	#--------
	def __init__(self, generics=NamedObjList(), ports=NamedObjList(),
		decls=NamedObjList(), archs=NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		Base.__init__(self, src_loc_at=src_loc_at + 1)
		HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(ports, NamedObjList), \
			type(ports)
		self.__ports = ports

		# declarations
		assert isinstance(decls, NamedObjList), \
			type(decls)
		self.__decls = decls

		# architectures
		assert isinstance(archs, NamedObjList), \
			type(archs)
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
	def visit(self, visitor):
		visitor.visitEntity(self)
	#--------
#--------
class Arch(Base, HasNameBase):
	#--------
	def __init__(self, decls=NamedObjList(), body=NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		Base.__init__(self, src_loc_at=src_loc_at + 1)
		HasNameBase.__init__(self, name=name)
		#--------
		# declarations
		assert isinstance(decls, NamedObjList), \
			type(decls)
		self.__decls = decls

		# Unlabelled statements body
		assert isinstance(body, NamedObjList), \
			type(body)
		self.__body = body
		#--------
	#--------
	def decls(self):
		return self.__decls
	def body(self):
		return self.__body
	#--------
	def visit(self, visitor):
		visitor.visitArch(self)
	#--------
#--------
class Package(Base, HasNameBase):
	#--------
	def __init__(self, generics=NamedObjList(), decls=NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		Base.__init__(self, src_loc_at=src_loc_at + 1)
		HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(decls, NamedObjList), \
			type(decls)
		self.__decls = decls
		#--------
	#--------
	def generics(self):
		return self.__generics
	def decls(self):
		return self.__decls
	#--------
	def visit(self, visitor):
		visitor.visitPackage(self)
	#--------
class PackageBody(Base, HasNameBase):
	#--------
	def __init__(self, decls=NamedObjList(), *, name="", src_loc_at=1):
		#--------
		Base.__init__(self, src_loc_at=src_loc_at + 1)
		HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(decls, NamedObjList), \
			type(decls)
		self.__decls = decls
		#--------
	#--------
	def decls(self):
		return self.__decls
	#--------
	def visit(self, visitor):
		visitor.visitPackageBody(self)
	#--------
#--------
