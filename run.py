# generic command-line argument aprser
import sys, json
def json_or_str(v):
	try:
		return json.loads(v)
	except:
		return str(v)
kargs, kwargs = [], {}
for arg in sys.argv[1:]:
	if arg.find('='):
		k,v = arg.split('=', maxsplit=2)
		kwargs[json_or_str(k)] = json_or_str(v)
	else:
		kargs.append(arg)

# pass arguments and start flask app
from app import app
app.run(*kargs, **kwargs)
