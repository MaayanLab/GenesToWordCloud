# generic command-line argument aprser
import sys
kargs, kwargs = [], {}
for arg in sys.argv[1:]:
	if arg.find('='):
		k,v = arg.split('=', maxsplit=2)
		try:
			kwargs[k] = eval(v)
		except:
			kwargs[k] = v
	else:
		kargs.append(arg)

# pass arguments and start flask app
from app import app
app.run(*kargs, **kwargs)
