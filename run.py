#!/usr/local/bin/python3

import sys
kargs, kwargs = [], {}
for arg in sys.argv[1:]:
	if arg.find('='):
		k,v = arg.split('=', maxsplit=2)
		kwargs[k] = v
	else:
		kargs.append(arg)

from app import app
app.run(*kargs, **kwargs)
