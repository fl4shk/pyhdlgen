#!/usr/bin/env python3

import sys

#--------
class Blank:
	pass

def psconcat(*args):
	return str().join([str(arg) for arg in args])

def lsconcat(lst):
	return str().join([str(elem) for elem in lst])

def fprintout(file, *args, flush=False):
	print(psconcat(*args), sep="", end="", file=file, flush=flush)

def printout(*args):
	fprintout(sys.stdout, *args)

def printerr(*args):
	fprintout(sys.stderr, *args)

def convert_enum_to_str(to_conv):
	return str(to_conv)[str(to_conv).find(".") + 1:]

def convert_str_to_enum_opt(to_conv, EnumT, STR_ENUM_MAP):
	assert (isinstance(to_conv, EnumT) or isinstance(to_conv, str)), \
		type(to_conv)

	if isinstance(to_conv, EnumT):
		return to_conv
	else: # if isinstance(to_conv, str):
		assert (to_conv in STR_ENUM_MAP), \
			to_conv
		return STR_DIRECTION_MAP[to_conv]
#--------
class NameDict:
	#--------
	def __init__(self, dct={}):
		self.__dct = dct
	#--------
	def dct(self):
		return self.__dct
	#--------
	def __getattr__(self, key):
		return self[key]
	def __getitem__(self, key):
		if NameDict.key_goes_in_dct(key):
			return self.__dct[key]
		else: # if not NameDict.key_goes_in_dct(key)
			return self.__dict__[key]

	def __setattr__(self, key, val):
		self[key] = val
	def __setitem__(self, key, val):
		if NameDict.key_goes_in_dct(key):
			self.__dct[key] = val
		else: # if not NameDict.key_goes_in_dct(key)
			self.__dict__[key] = val

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
	@staticmethod
	def key_goes_in_dct(key):
		return (isinstance(key, str) and (len(key) > 0) 
			and key[0].isalpha())
	#--------
#--------
