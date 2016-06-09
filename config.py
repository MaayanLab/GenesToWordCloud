from pymysql.cursors import DictCursor

config = {
	'database': 'DRIVER={SQL Server};SERVER=localhost;PORT=;DATABASE=;UID=me;PWD=pass;',
	'query_limit': 150,
	'pubmed_query_limit': 10,
	'word_cloud': {
		'max_width': 1920,
		'max_height': 1200,
	},
}
