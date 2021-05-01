#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_misc_ast import *
from vhdl_misc_ast import *
from vhdl_expr_ast import *

from enum import Enum, auto
#--------
class Component(_Base, HasNameBase):
	#--------
	def __init__(self, generics=NamedObjList(), ports=NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		_Base.__init__(self, src_loc_at=src_loc_at + 1)
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
class Entity(_Base, HasNameBase):
	#--------
	def __init__(self, generics=NamedObjList(), ports=NamedObjList(),
		decls=NamedObjList(), archs=NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		_Base.__init__(self, src_loc_at=src_loc_at + 1)
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
class Arch(_Base, HasNameBase):
	#--------
	def __init__(self, decls=NamedObjList(), body=NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		_Base.__init__(self, src_loc_at=src_loc_at + 1)
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
class Package(_Base, HasNameBase):
	#--------
	def __init__(self, generics=NamedObjList(), decls=NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		_Base.__init__(self, src_loc_at=src_loc_at + 1)
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
class PackageBody(_Base, HasNameBase):
	#--------
	def __init__(self, decls=NamedObjList(), *, name="", src_loc_at=1):
		#--------
		_Base.__init__(self, src_loc_at=src_loc_at + 1)
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
class Use(_Base):
	def __init__(self, sel_name_lst=[], *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(sel_name_lst, list), \
			type(sel_name_lst)
		for sel_name in sel_name_lst:
			assert isinstance(sel_name, SelName), \
				type(sel_name)

		self.__sel_name_lst = sel_name_lst
	def sel_name_lst(self):
		return self.__sel_name_lst
	def visit(self, visitor):
		visitor.visitUse(self)
class SelName(_Base):
	#--------
	def __init__(self, prefix, suffix, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert (isinstance(prefix, str)
			or isinstance(prefix, CallFunction)), \
			type(prefix)
		self.__prefix = prefix

		assert (isinstance(suffix, str) or isinstance(suffix, CharLiteral)
			or isinstance(suffix, StrLiteral)
			or isinstance(suffix, All)), \
			type(suffix)
		self.__suffix = suffix
		#--------
	#--------
	def prefix(self):
		return self.__prefix
	def suffix(self):
		return self.__suffix
	#--------
	def visit(self, visitor):
		visitor.visitSelName(self)
	#--------
#--------
