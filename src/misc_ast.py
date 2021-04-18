#!/usr/bin/env python3

#--------
from misc_util import *
from tracer import *

from enum import Enum, auto
#import inspect
#--------
class Base:
	#--------
	def __init__(self, *, src_loc_at=1):
		frame = inspect.stack()[src_loc_at].frame
		getframeinfo_ret = inspect.getframeinfo(frame)
		self.__filename = getframeinfo_ret.filename
		self.__lineno = getframeinfo_ret.lineno
		pass
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
