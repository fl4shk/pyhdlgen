#!/usr/bin/env python3

#--------
import inspect
#--------
def get_src_loc(src_loc_at=0):
	# n-th frame:  get_src_loc()
	# n-1th frame:  caller of `get_src_loc()` (usually constructor)
	# n-2th frame:  caller of caller (usually user code)
	stack = inspect.stack()
	frame = stack[src_loc_at + 2].frame
	return (frame.f_code.co_filename, frame.f_lineno)
#--------
