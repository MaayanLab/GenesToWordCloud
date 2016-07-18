'''
Expose database table querying for keywords as python functions
'''

import pymysql
from config import config
from pubmed import pubmed_query

def query(what, table, genes):
	con = pymysql.connect(**config['database'])
	cur = con.cursor()
	cur.execute('select '
		+(','.join(what) if type(what)==list else what)
		+' from '+table
		+' where '+(' or '.join(['geneName=%s' for gene in genes]))
		+' order by rand() limit '+str(config['query_limit']), genes)
	return cur.fetchall()


tables = {}
def register_table(func):
	tables[func.__name__] = func
	return func


@register_table
def generif(genes):
	for row in query(['generif', 'pmid'], 'generif', genes):
		yield(row['generif'])
		# yield(pubmed_query(search=False, id=row['pmid']))

@register_table
def pubmed(genes):
	for row in query('pmid', 'pmid_symbol', genes):
		yield(pubmed_query(search=False, id=row['pmid']))

@register_table
def go(genes):
	for row in query(['go','goID'], 'go', genes):
		yield(row['go'])
		# TODO: yield(go_query(id=row['goID']))

@register_table
def mp(genes):
	''' TODO '''
	for row in query('mp, mpID', 'mp', genes):
		yield(row['mp'])
		# TODO: yield(mp_query(id=row['mpID']))
