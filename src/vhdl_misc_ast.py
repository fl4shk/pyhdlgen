#!/usr/bin/env python3

#--------
from misc_util import *
#from vhdl_expr_ast import *
#import vhdl_expr_ast as expr_ast
#import vhdl_type_ast as type_ast
#from vhdl_expr_ast import *

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
	#--------
	def filename(self):
		return self.__filename
	def lineno(self):
		return self.__lineno
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
#--------
class NamedObjDict(Base):
	#--------
	def __init__(self, dct=NameDict(), *, src_loc_at=1):
		super().__init__(src_loc_at=src_loc_at + 1)

		self.__dct = dct
	#--------
	def dct(self):
		return self.__dct
	#--------
	def __getattr__(self, key):
		return self[key]
	def __getitem__(self, key):
		return self.dct()[key]

	def __setattr__(self, key, val):
		self[key] = val
	def __setitem__(self, key, val):
		self.dct()[key] = val

		assert hasattr(self.dct()[key], "_set_name")

		self.dct()[key]._set_name(key)

	def __iadd__(self, val):
		self.dct() += val
	#--------
#--------
