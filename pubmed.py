'''
Application Interface for querying the pubmed database
'''

import urllib.request
import itertools as it
from bs4 import BeautifulSoup
from config import config

def pubmed_query(search=True, **kwargs):
	''' API for querying the pubmed database via GET requests '''
	# default parameters, overridden by **kwargs
	params = dict({'retmode': 'xml',
				   'rettype': 'Abstract',
				   'db': 'pubmed',
				   'retmax': config['pubmed_query_limit']},
				   **kwargs)

	# create url serializing kwargs in GET
	url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/e%s.fcgi?%s' % (
		'search' if search else 'fetch',
		'&'.join('='.join(map(str, param))
				  for param in params.items()))

	# open and parse the website
	xml = urllib.request.urlopen(url)
	soup = BeautifulSoup(xml, 'xml')

	# search or fetch
	if search:
		# perform a pubmed query on each id in our results
		return ' '.join(pubmed_query(search=False, id=i.getText())
									  for i in soup.findAll('Id'))
	else:
		# return the text in the title/abstract
		return ' '.join(res.getText()
						for section in ['ArticleTitle', 'AbstractText']
						for res in soup.findAll(section))
