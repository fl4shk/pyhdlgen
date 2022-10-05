#!/usr/bin/env python3

#--------
from misc_util import *

from enum import Enum, auto
import inspect
#--------
class Base:
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
		assert isinstance(n_parent, Base), \
			do_type_assert_psconcat(n_parent)
		self.__parent = n_parent
	def parent(self):
		return self.__parent
	#--------
	def visit(self, visitor):
		visitor.visitBase(self)
	#--------
#--------
# Comment
class Com(Base):
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
class Others(Base):
	def __init__(self, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)
	def visit(self, visitor):
		visitor.visitOthers(self)
class All(Base):
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
class NamedObjList(Base):
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
			assert isinstance(val, Base), \
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
		assert (isinstance(val, Base) or isinstance(val, tuple)), \
			type(val)

		if isinstance(val, Base):
			self.lst().append(val)
			return self.lst()[-1]
		else: # if isinstance(val, tuple):
			assert (len(val) == 2), \
				len(val)
			assert isinstance(val[0], str), \
				do_type_assert_psconcat(val[0])
			assert isinstance(val[1], Base), \
				do_type_assert_psconcat(val[1])
			self[val[0]] = val[1]
			return self[val[0]]

	def __iadd__(self, val):
		assert (isinstance(val, list) or isinstance(val, Base)
			or isinstance(val, tuple)), \
			do_type_assert_psconcat(val)

		if isinstance(val, list):
			for elem in val:
				self.append(elem)
		else: # if isinstance(val, Base) or isinstance(val, tuple):
			self.append(val)
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
#		assert isinstance(val, BehavStmt), \
#			do_assert_psconcat(val)
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
