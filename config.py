from pymysql.cursors import DictCursor

config = {
	'database': {
		'host': 'localhost',
		'user': '',
		'password': '',
		'db': 'db',
		'charset': '',
		'cursorclass': DictCursor,
	},
	'query_limit': 150,
	'pubmed_query_limit': 10,
	'word_cloud': {
		'max_width': 1920,
		'max_height': 1200,
	},
}
