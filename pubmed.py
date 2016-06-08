import itertools
import urllib.request
from bs4 import BeautifulSoup

def pubmed_query(**kwargs):
	params = dict({'retmode': 'xml',
				   'db': 'pubmed',
				   'retmax': 10},
				   **kwargs)
	url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?%s' % (
		'&'.join(['='.join(map(str, param))
				  for param in params.items()]))
	xml = urllib.request.urlopen(url)
	soup = BeautifulSoup(xml, 'xml')
	if 'id' not in kwargs.keys():
		return itertools.chain.from_iterable(
			[pubmed_query(id=i.getText())
			 for i in i_soup.find('IdList').findAll('Id')])
	else:
		return itertools.chain.from_iterable(
			[[res.getText().strip()
			  for res in soup.findAll(section)]
			 for section in ['ArticleTitle', 'AbstractText']])
