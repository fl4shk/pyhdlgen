#!/usr/bin/env python3

#--------
from misc_util import *

import vhdl_ast.vhdl_ast as ast

from enum import Enum, auto
#--------
# configuration_declaration
class ConfigDecl(ast.Base, ast.HasNameBase):
	#--------
	def __init__(self, decls=ast.NamedObjList(),
		block_config=BlockConfig(), entity, *, name="", src_loc_at=1):
		#--------
		ast.Base.__init__(self, src_loc_at=src_loc_at + 1)
		ast.HasNameBase.__init__(self, name=name)
		#--------
		self.__decls = decls

		assert isinstance(block_config, BlockConfig), \
			do_type_assert_psconcat(block_config)
		self.__block_config = block_config

		assert isinstance(entity, ast.Entity), \
			do_type_assert_psconcat(entity)
		self.__entity = entity
		#--------
	#--------
	def decls(self):
		return self.__decls
	def block_config(self):
		return self.__block_config
	def entity(self):
		return self.__entity
	#--------
	def visit(self, visitor):
		visitor.visitConfigDecl(self)
	#--------
# block_configuration
class BlockConfig(ast.Base):
	#--------
	def __init__(self, use_clause_lst=[], config_item_lst=[], *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(use_clause_lst, list), \
			do_type_assert_psconcat(use_clause_lst)
		for i in range(len(use_clause_lst)):
			elem = use_clause_lst[i]
			assert isinstance(elem, ast.UseClause), \
				do_type_assert_psconcat(elem)
		self.__use_clause_lst = use_clause_lst

		assert isinstance(config_item_lst, list), \
			do_type_assert_psconcat(config_item_lst)
		for i in range(len(config_item_lst)):
			elem = config_item_lst[i]
			assert (isinstance(elem, BlockConfig)
				or isinstance(elem, ComponentConfig)), \
				do_type_assert_psconcat(elem)
		self.__config_item_lst = config_item_lst
		#--------
	#--------
	def use_clause_lst(self):
		return self.__use_clause_lst
	def config_item_lst(self):
		return self.__config_item_lst
	#--------
	def visit(self, visitor):
		visitor.visitBlockConfig(self)
	#--------
# component_configuration
class ComponentConfig(ast.Base):
	#--------
	def __init__(self, binding_indic=None, block_config=None, *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert ((binding_indic is None)
			or isinstance(binding_indic, BindingIndic)), \
			do_type_assert_psconcat(binding_indic)
		self.__binding_indic = binding_indic

		assert ((block_config is None)
			or isinstance(block_config, BlockConfig)), \
			do_type_assert_psconcat(block_config)
		self.__block_config = block_config
		#--------
	#--------
	def binding_indic(self):
		return self.__binding_indic
	def block_config(self):
		return self.__block_config
	#--------
	def visit(self, visitor):
		visitor.visitComponentConfig(self)
	#--------
#--------
class BindingIndic(ast.Base):
	#--------
	def __init__(self, obj=None, generic_map=None, port_map=None, *,
		src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert ((obj is None) or isinstance(obj, ast.Entity)
			or isinstance(obj, ast.Arch) or isinstance(obj, ConfigDecl)
			or isinstance(obj, ast.Open)), \
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
		visitor.visitBindingIndic(self)
	#--------
#--------
class ConfigSpecBase(ast.Base):
	#--------
	def __init__(self, component_spec, binding_indic, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(component_spec, ComponentSpec), \
			do_type_assert_psconcat(component_spec)
		self.__component_spec = component_spec

		assert isinstance(binding_indic, BindingIndic), \
			do_type_assert_psconcat(binding_indic)
		self.__binding_indic = binding_indic
		#--------
	#--------
	def component_spec(self):
		return self.__component_spec
	def binding_indic(self):
		return self.__binding_indic
	#--------
	def visit(self, visitor):
		visitor.visitConfigSpecBase(self)
	#--------
# simple_configuration_specification
class SmplConfigSpec(ConfigSpecBase):
	def __init__(self, component_spec, binding_indic, *, src_loc_at=1):
		super().__init__(component_spec, binding_indic,
			src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitSmplConfigSpec(self)
# component_specification
class ComponentSpec(ast.Base):
	#--------
	def __init__(self, inst_lst, component, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert (isinstance(inst_lst, list)
			or isinstance(inst_lst, ast.Others)
			or isinstance(inst_lst, ast.All)), \
			do_type_assert_psconcat(inst_lst)

		if isinstance(inst_lst, list):
			for i in range(len(inst_lst)):
				inst = inst_lst[i]
				assert (isinstance(inst, ast.Component)
					or isinstance(inst, ast.Entity)
					or isinstance(inst, ast.Arch)
					or isinstance(inst, ast.ConfigDecl)), \
					do_type_assert_psconcat(inst, i, inst_lst)
		self.__inst_lst = inst_lst

		assert isinstance(component, ast.Component), \
			do_type_assert_psconcat(component)
		self.__component = component
		#--------
	#--------
	def inst_lst(self):
		return self.__inst_lst
	def component(self):
		return self.__component
	#--------
	def visit(self, visitor):
		visitor.visitComponentSpec(self)
	#--------
#--------
