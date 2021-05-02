#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_misc_ast import *
#from vhdl_misc_ast import *
#from vhdl_expr_ast import *
import vhdl_ast.vhdl_ast as vhdl_ast

from enum import Enum, auto
#--------
class Component(vhdl_ast.Base, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, generics=vhdl_ast.NamedObjList(),
		ports=vhdl_ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, vhdl_ast.NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(ports, vhdl_ast.NamedObjList), \
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
class Entity(vhdl_ast.Base, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, generics=vhdl_ast.NamedObjList(),
		ports=vhdl_ast.NamedObjList(), decls=vhdl_ast.NamedObjList(),
		archs=vhdl_ast.NamedObjList(), *, name="", src_loc_at=1):
		#--------
		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, vhdl_ast.NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(ports, vhdl_ast.NamedObjList), \
			type(ports)
		self.__ports = ports

		# declarations
		assert isinstance(decls, vhdl_ast.NamedObjList), \
			type(decls)
		self.__decls = decls

		# architectures
		assert isinstance(archs, vhdl_ast.NamedObjList), \
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
class Arch(vhdl_ast.Base, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, decls=vhdl_ast.NamedObjList(),
		body=vhdl_ast.NamedObjList(), *,
		name="", src_loc_at=1):
		#--------
		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
		# declarations
		assert isinstance(decls, vhdl_ast.NamedObjList), \
			type(decls)
		self.__decls = decls

		# Unlabelled statements body
		assert isinstance(body, vhdl_ast.NamedObjList), \
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
class Package(vhdl_ast.Base, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, generics=vhdl_ast.NamedObjList(),
		decls=vhdl_ast.NamedObjList(), *, name="", src_loc_at=1):
		#--------
		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, vhdl_ast.NamedObjList), \
			type(generics)
		self.__generics = generics

		assert isinstance(decls, vhdl_ast.NamedObjList), \
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
class PackageBody(vhdl_ast.Base, vhdl_ast.HasNameBase):
	#--------
	def __init__(self, decls=vhdl_ast.NamedObjList(), *, name="",
		src_loc_at=1):
		#--------
		vhdl_ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		vhdl_ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(decls, vhdl_ast.NamedObjList), \
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
class Use(vhdl_ast.Base):
	def __init__(self, sel_name_lst=[], *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(sel_name_lst, list), \
			type(sel_name_lst)
		for sel_name in sel_name_lst:
			assert isinstance(sel_name, vhdl_ast.SelName), \
				type(sel_name)

		self.__sel_name_lst = sel_name_lst
	def sel_name_lst(self):
		return self.__sel_name_lst
	def visit(self, visitor):
		visitor.visitUse(self)
#--------
