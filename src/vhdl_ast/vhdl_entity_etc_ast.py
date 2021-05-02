#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
class Component(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, generics=ast.NamedObjList(),
		ports=ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, ast.NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(ports, ast.NamedObjList), \
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
class Entity(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, generics=ast.NamedObjList(),
		ports=ast.NamedObjList(), decls=ast.NamedObjList(),
		archs=ast.NamedObjList(), *, name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, ast.NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(ports, ast.NamedObjList), \
			type(ports)
		self.__ports = ports

		# declarations
		assert isinstance(decls, ast.NamedObjList), \
			type(decls)
		self.__decls = decls

		# architectures
		assert isinstance(archs, ast.NamedObjList), \
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
class Arch(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, decls=ast.NamedObjList(),
		body=ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		# declarations
		assert isinstance(decls, ast.NamedObjList), \
			type(decls)
		self.__decls = decls

		# Unlabelled statements body
		assert isinstance(body, ast.NamedObjList), \
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
class Package(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, decls=ast.NamedObjList(), is_extern=False, *,
		name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		#assert isinstance(generics, ast.NamedObjList), \
		#	type(generics)
		#self.__generics = generics

		assert isinstance(decls, ast.NamedObjList), \
			type(decls)
		self.__decls = decls

		self.__is_extern = is_extern
		#--------
	#--------
	#def generics(self):
	#	return self.__generics
	def decls(self):
		return self.__decls
	def is_extern(self):
		return self.__is_extern
	#--------
	def visit(self, visitor):
		visitor.visitPackage(self)
	#--------
class PackageBody(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, decls=ast.NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(decls, ast.NamedObjList), \
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
class Use(ast.Base):
	def __init__(self, sel_name_lst=[], *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(sel_name_lst, list), \
			type(sel_name_lst)
		for sel_name in sel_name_lst:
			assert isinstance(sel_name, ast.SelName), \
				type(sel_name)

		self.__sel_name_lst = sel_name_lst
	def sel_name_lst(self):
		return self.__sel_name_lst
	def visit(self, visitor):
		visitor.visitUse(self)
#--------
