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
#--------
class NameDict:
	#--------
	def __init__(self, dct={}):
		self.__dct = dct
	#--------
	def dct(self):
		return self.__dct
	#--------
	def __getattr__(self, name):
		return self[name]
	def __getitem__(self, name):
		if self.__name_goes_in_dct(name):
			return self.__dct[name]
		else: # if not self.__name_goes_in_dct(name)
			return self.__dict__[name]

	def __setattr__(self, name, val):
		self[name] = val
	def __setitem__(self, name, val):
		if self.__name_goes_in_dct(name):
			self.__dct[name] = val
		else: # if not self.__name_goes_in_dct(name)
			self.__dict__[name] = val
	#--------
	def __name_goes_in_dct(self, name):
		return (isinstance(name, str) and (len(name) > 0) 
			and name[0].isalpha())
	#--------
#--------
