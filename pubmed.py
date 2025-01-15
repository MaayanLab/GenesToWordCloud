'''
Application Interface for querying the pubmed database

Future Direction: This just caches terms but it would be even better to cache word frequencies (processed),
  this will require some reorginization of the code however as pubmed_query would need to return processed
  results rather than a big word list.
'''

import pymysql
import urllib.request, urllib.parse
import traceback
from bs4 import BeautifulSoup
from config import config

def pubmed_cache(pmid):
	''' Cache results for general speedups of pubmed queries '''
	con = pymysql.connect(**config['database'])
	cur = con.cursor()
	cur.execute('select terms from pubmed_cache where pmid=%s', (pmid))
	res = cur.fetchall()
	if res:
		print('h')
		terms = ' '.join(urllib.parse.unquote(t['terms']) for t in res)
	else:
		print('m')
		try:
			terms = pubmed_query(search=False, id=pmid)
			if terms:
				cur.execute('insert into pubmed_cache values (%s, %s)', (pmid, urllib.parse.quote(terms)))
				con.commit()
		except KeyboardInterrupt: raise
		except:
			traceback.print_exc()
			terms = ''
	return terms

def pubmed_query(search=True, **kwargs):
	''' API for querying the pubmed database via GET requests '''
	try:
		# default parameters, overridden by **kwargs
		params = dict({'retmode': 'xml',
					   'rettype': 'Abstract',
					   'db': 'pubmed',
					   'retmax': config['pubmed_query_limit']},
					   **kwargs)

		# create url serializing kwargs in GET
		
		url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/e%s.fcgi?%s' % (
			'search' if search else 'fetch',
			urllib.parse.urlencode(params))

		# open and parse the website
		xml = urllib.request.urlopen(url)
		soup = BeautifulSoup(xml, 'xml')

		# search or fetch
		if search:
			# perform a pubmed query on each id in our results
			return ' '.join(pubmed_cache(i.getText()) # pubmed_query(search=False, id=i.getText())
							for i in soup.findAll('Id'))
		else:
			# return the text in the title/abstract
			return ' '.join(res.getText()
							for section in ['ArticleTitle', 'AbstractText']
							for res in soup.findAll(section))
	except KeyboardInterrupt: raise
	except:
		traceback.print_exc()
		return ''
