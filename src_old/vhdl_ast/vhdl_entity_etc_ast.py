#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
class Component(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, generics=ast.NamedObjList(),
		ports=ast.NamedObjList(), *, name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert isinstance(generics, ast.NamedObjList), \
			do_type_assert_psconcat(generics)
		self.__generics = generics

		assert isinstance(ports, ast.NamedObjList), \
			do_type_assert_psconcat(ports)
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
			do_type_assert_psconcat(generics)
		self.__generics = generics

		assert isinstance(ports, ast.NamedObjList), \
			do_type_assert_psconcat(ports)
		self.__ports = ports

		# declarations
		assert isinstance(decls, ast.NamedObjList), \
			do_type_assert_psconcat(decls)
		self.__decls = decls

		# architectures
		assert isinstance(archs, ast.NamedObjList), \
			do_type_assert_psconcat(archs)
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
	def __init__(self, decls=ast.NamedObjList(), body=ast.NamedObjList(),
		*, name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		# declarations
		assert isinstance(decls, ast.NamedObjList), \
			do_type_assert_psconcat(decls)
		self.__decls = decls

		# Unlabelled statements body
		assert isinstance(body, ast.NamedObjList), \
			do_type_assert_psconcat(body)
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
class Instance(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, obj, generic_map=None, port_map=None, *, name="",
		src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		assert (isinstance(obj, Component) or isinstance(obj, Entity)
			or isinstance(obj, Arch) or isinstance(obj, ast.ConfigDecl)), \
			do_type_assert_psconcat(obj)
		self.__obj = obj

		assert ((generic_map is None)
			or isinstance(generic_map, ast.GenericMap)), \
			do_type_assert_psconcat(generic_map)
		self.__generic_map = generic_map

		assert ((port_map is None)
			or isinstance(port_map, ast.PortMap)), \
			do_type_assert_psconcat(port_map)
		self.__port_map = port_map
		#--------
	#--------
	def obj(self):
		return self.__obj
	def generic_map(self):
		return self.__generic_map
	def port_map(self):
		return self.__port_map
	#--------
	def visit(self, visitor):
		visitor.visitInstance(self)
	#--------
#--------
