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
#--------
class NamedObjDict(Base):
	#--------
	def __init__(self, dct={}, *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		assert isinstance(dct, dict), \
			type(dct)
		self.__dct = dct
	#--------
	def dct(self):
		return self.__dct
	#--------
	def visit(self, visitor):
		visitor.visitNamedObjDict(self)
	#--------
	def __getattr__(self, key):
		return self[key]
	def __getitem__(self, key):
		if NameDict.key_goes_in_dct(key):
			return self.dct()[key]
		else: # if not NameDict.key_goes_in_dct(keys):
			return self.__dict__[key]

	def __setattr__(self, key, val):
		self[key] = val
	def __setitem__(self, key, val):
		if NameDict.key_goes_in_dct(key):
			assert isinstance(val, Base), \
				type(val)

			self.dct()[key] = val

			assert hasattr(self.dct()[key], "_set_name")
			self.assert_valid_val(val)

			self.dct()[key]._set_name(key)
		else: # if not NameDict.key_goes_in_dct(key):
			self.__dict__[key] = val

	def assert_valid_val(self, val):
		pass

	def __iadd__(self, val):
		assert (isinstance(val, list) or isinstance(val, tuple)), \
			type(val)

		if isinstance(val, list):
			for item in val:
				assert isinstance(item, tuple) and (len(item) == 2)
				self[item[0]] = item[1]
		else: # if isinstance(val, tuple):
			assert (len(item) == 2), \
				str(len(item))
			self[val[0]] = val[1]
	#--------
## FIXME:  These need to be adjusted once I remember what the problem with
## just using `NamedObjDict` was
#class BehavStmtNod(NamedObjDict):
#	#--------
#	def __init__(self, dct=NameDict(), *, src_loc_at=1):
#		super().__init__(dct, src_loc_at=src_loc_at + 1)
#	#--------
#	def visit(self, visitor):
#		visitor.visitBehavStmtNod(self)
#	#--------
#	def assert_valid_val(self, val):
#		assert isinstance(val, BehavStmt), \
#			type(val)
#	#--------
## This is not a class to contain `DeclComponent` and friends, but it is to
## be their `decls` component.
#class DeclsNod(NamedObjDict):
#	#--------
#	def __init__(self, dct=NameDict(), *, src_loc_at=1):
#		super().__init__(dct, src_loc_at=src_loc_at + 1)
#	#--------
#	def visit(self, visitor):
#		visitor.visitDeclsNod(self)
#	#--------
#	def assert_valid_val(self, val):
#		assert isinstance(val, )
#	#--------
