'''
Global application configuration options
'''

import os
import urllib.parse
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
load_dotenv()

database_url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
assert database_url.scheme in {'mysql', 'mariadb'}
database = dict(
	host=database_url.hostname,
  user=database_url.username,
  password=database_url.password,
  database=database_url.path.lstrip('/'),
  port=database_url.port or 3306,
  cursorclass=DictCursor,
)

config = {
	'database': database,
	'query_limit': 150,
	'pubmed_query_limit': 10
}
