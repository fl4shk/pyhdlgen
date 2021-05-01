#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_expr_ast import *
#import vhdl_expr_ast as expr_ast
#import vhdl_type_ast as type_ast
#from vhdl_expr_ast import *
from vhdl_behav_ast import *
from vhdl_concur_ast import *

from enum import Enum, auto
import inspect
#--------
class _Base:
	#--------
	def __init__(self, *, src_loc_at=1):
		frame = inspect.stack()[src_loc_at].frame

		getframeinfo_ret = inspect.getframeinfo(frame)

		self.__filename = getframeinfo_ret.filename
		self.__lineno = getframeinfo_ret.lineno

		self.__parent = None
	#--------
	def filename(self):
		return self.__filename
	def lineno(self):
		return self.__lineno
	def _set_parent(self, n_parent):
		assert isinstance(n_parent, _Base), \
			type(n_parent)
		self.__parent = n_parent
	def parent(self):
		return self.__parent
	#--------
	def visit(self, visitor):
		visitor.visitBase(self)
	#--------
#--------
# Comment
class Com(_Base):
	#--------
	def __init__(self, val, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		assert isinstance(val, str), \
			type(val)
		self.__val = val
		#--------
	#--------
	def val(self):
		return self.__val
	#--------
	def visit(self, visitor):
		visitor.visitCom(self)
	#--------
class Others(_Base):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitOthers(self)
class All(_Base):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitAll(self)
#--------
class HasNameBase:
	#--------
	def __init__(self, *, name=""):
		self._set_name(name)
	#--------
	def _set_name(self, n_name):
		assert isinstance(n_name, str), \
			type(n_name)
		self.__name = n_name.lower()
	def name(self):
		return self.__name
	#--------
class NamedObjList(_Base):
	#--------
	def __init__(self, *, src_loc_at=1):
		#--------
		super().__init__(src_loc_at=src_loc_at + 1)
		#--------
		self.__lst = []
		self.__name_to_ind_map = {}
		#--------
	#--------
	def lst(self):
		return self.__lst
	def name_to_ind_map(self):
		return self.__name_to_ind_map
	#--------
	def __getattr__(self, key):
		return self[key]
	def __getitem__(self, key):
		if NameDict.key_goes_in_dct(key):
			return self.lst()[self.name_to_ind_map(key.lower())][1]
		else: # if not NameDict.key_goes_in_dct(key):
			return self.__dict__[key]

	def __setattr__(self, key, val):
		self[key] = val
	def __setitem__(self, key, val):
		if NameDict.key_goes_in_dct(key):
			assert isinstance(val, _Base), \
				type(val)
			assert isinstance(val, HasNameBase), \
				type(val)

			temp_key = key.lower()

			self.assert_valid_val(val)

			if temp_key not in self.name_to_ind_map():
				ind = len(self.lst())
				self.name_to_ind_map()[temp_key] = ind
				self.append(val)
			else: # if temp_key i in self.name_to_ind_map():
				ind = self.name_to_ind_map()[temp_key]
				self.lst()[ind] = val

			self.lst()[ind]._set_name(temp_key)
		else: # if not NameDict.key_goes_in_dct(key):
			self.__dict__[key] = val

	def assert_valid_val(self, val):
		pass

	def append(self, val):
		assert (isinstance(elem, _Base) or isinstance(elem, tuple)), \
			type(elem)

		if isinstance(elem, _Base):
			self.lst().append(val)
			return self.lst()[-1]
		else: # if isinstance(elem, tuple):
			assert (len(elem) == 2), \
				len(elem)
			assert isinstance(elem[0], str), \
				type(elem[0])
			assert isinstance(elem[1], _Base), \
				type(elem[1])
			self[elem[0]] = elem[1]
			return self[elem[0]]

	def __iadd__(self, val):
		assert isinstance(val, list), \
			type(val)

		for elem in val:
			self.append(elem)
	#--------
## FIXME:  These need to be adjusted once I remember what the problem with
## just using `NamedObjList` was
#class BehavStmtNol(NamedObjList):
#	#--------
#	def __init__(self, dct=NameDict(), *, src_loc_at=1):
#		super().__init__(dct, src_loc_at=src_loc_at + 1)
#	#--------
#	def visit(self, visitor):
#		visitor.visitBehavStmtNol(self)
#	#--------
#	def assert_valid_val(self, val):
#		assert isinstance(val, _BehavStmt), \
#			type(val)
#	#--------
## This is not a class to contain `DeclComponent` and friends, but it is to
## be their `decls` component.
#class DeclsNol(NamedObjList):
#	#--------
#	def __init__(self, dct=NameDict(), *, src_loc_at=1):
#		super().__init__(dct, src_loc_at=src_loc_at + 1)
#	#--------
#	def visit(self, visitor):
#		visitor.visitDeclsNol(self)
#	#--------
#	def assert_valid_val(self, val):
#		assert isinstance(val, )
#	#--------
