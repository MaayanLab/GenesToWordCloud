'''
Global application configuration options
'''

import json
from pymysql.cursors import DictCursor

config = {
	'database': dict(json.load(open('db.conf', 'r')), cursorclass=DictCursor),
	'query_limit': 150,
	'pubmed_query_limit': 10
}

