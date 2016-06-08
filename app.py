import re
import urllib
import random
import itertools
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request
from word_cloud import process_page
from pubmed import pubmed_query

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/help')
def help():
	return render_template('help.html')


def route_page(func):
	name = func.__name__
	def create():
		return render_template('create/%s.html' % (name), cloud_type=name)
	app.add_url_rule('/create/%s' % (name), 'create_%s' % (name), create)
	app.add_url_rule('/view/%s' % (name), 'view_%s' % (name), func, methods=['GET'])

@route_page
def genes():
	genes = request.args.get('genes')
	if not genes:
		return None

	source = request.args.get('source')
	if source == "generif":
		#  $query = "SELECT generif, pmid FROM generif WHERE".$query_ending."ORDER BY RAND(),pmid LIMIT ".$max_generifs;
		pass
	elif source == 'pubmed':
		# $query = "SELECT pmid FROM pmid_symbol WHERE".$query_ending." ORDER BY RAND() LIMIT ".$max_pmids;
		pass
	elif source == 'go':
		# $query = "SELECT go, goID FROM go WHERE".$query_ending."ORDER BY RAND(), goID LIMIT ".$max_go;
		pass
	elif source == 'mp':
		# $query = "SELECT mp, mpID FROM mp WHERE".$query_ending."ORDER BY RAND(), mp LIMIT ".$max_mp;
		pass
	elif source == 'mesh_terms':
		# $query = "SELECT pmid FROM pmid_symbol WHERE".$query_ending." ORDER BY RAND() LIMIT ".$max_pmids;
		pass
	
	# we need to look at the old database to better understand how this should work
	pass

@route_page
def free_text():
	text = request.args.get('text')
	if not text:
		return None
	return process_page(text, request.args)

@route_page
def url():
	url = request.args.get('url')
	if not url:
		return None
	html = urllib.request.urlopen(url)
	soup = BeautifulSoup(html, 'html.parser').find('html')
	for group in ['head', 'script', 'style']:
		for elem in soup.findAll(group):
			elem.extract()
	text = ' '.join(filter(None, map(str.strip, soup.findAll(text=True))))
	return process_page(text, request.args)

@route_page
def author():
	author = request.args.get('author')
	if not author:
		return None
	return process_page(pubmed_query(term='%s[Author]' % (author)), request.args)

@route_page
def pubmed():
	keyword = request.args.get('keyword')
	if not keyword:
		return None
	return process_page(pubmed_query(term=keyword), request.args)

@route_page
def bmc():
	date = request.args.get('date')
	if date == 'year':
		urllib.request.get('http://bmcbioinformatics.biomedcentral.com/articles/most-recent/rss.xml')
	elif date == 'ever':
		urllib.request.get('http://www.biomedcentral.com/mostviewedalltime/')
	else:
		urllib.request.get('http://www.biomedcentral.com/bmcbioinformatics/mostviewed/')
	# todo: get pubmed IDs from bmc page
	# we might need to be logged in for this to work
	pass
