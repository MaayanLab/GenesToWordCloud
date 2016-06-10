'''
Global application configuration options
'''

from pymysql.cursors import DictCursor

config = {
	'database': {
		'host': 'localhost',
		'user': '',
		'password': '',
		'db': 'db',
		'charset': 'utf8mb4',
		'cursorclass': DictCursor,
	},
	'query_limit': 150,
	'pubmed_query_limit': 10
}
