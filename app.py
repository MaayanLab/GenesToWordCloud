'''
Inform flask of the different pages available and do some basic preparation for process.py
'''

import urllib
import pymysql
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request
from process import process_page, error
from pubmed import pubmed_query
from config import config

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/help')
def help():
	return render_template('help.html')


def route_page(func):
	''' Decorator for different cloud generation pages,
	Automatically creates the `/create/name` page and points the
	 `/view/name` page to the function. '''
	name = func.__name__ # using the python name of the function passed
	def create():
		return render_template('create/%s.html' % (name), cloud_type=name)
	app.add_url_rule('/create/%s' % (name), 'create_%s' % (name), create)
	app.add_url_rule('/view/%s' % (name), 'view_%s' % (name), func, methods=['GET'])

@route_page
def genes():
	''' MySQL database lookup for gene names '''
	genes = request.args.get('genes')
	if not genes:
		return error()
	genes = genes.split()

	# prepare where clause
	where = 'where '+' or '.join(['geneName=%s' for gene in genes])

	source = request.args.get('source')
	if not source:
		return error()

	# connect to database
	con = pymysql.connect(**config['database'])
	cur = con.cursor()

	# query source
	if source == "generif":
		cur.execute('select generif, pmid from generif '+where+' order by rand(), pmid limit %s', (*genes, config['query_limit']))
		text = ' '.join([pubmed_query(search=False, id=row['pmid']) for row in cur.fetchall()])
	elif source == 'pubmed':
		cur.execute('select pmid from pmid_symbol '+where+' order by rand() limit %s', (*genes, config['query_limit']))
		text = ' '.join([pubmed_query(search=False, id=row['pmid']) for row in cur.fetchall()])
	elif source == 'go':
		cur.execute('select go, goID from go '+where+' order by rand(), goID limit %s', (*genes, config['query_limit']))
		text = ' '.join([row['go'] for row in cur.fetchall()])
	elif source == 'mp':
		cur.execute('select mp, mpID from mp '+where+' order by rand(), mp limit %s', (*genes, config['query_limit']))
		text = ' '.join([row['mp'] for row in cur.fetchall()])
	elif source == 'mesh_terms':
		cur.execute('select pmid from pmid_symbol where '+where+' order by rand() limit %s', (*genes, config['query_limit']))
		text = ' '.join([pubmed_query(search=False, id=row['pmid']) for row in cur.fetchall()])
	else:
		return error()

	con.close()

	return process_page(text, request.args)

@route_page
def free_text():
	text = request.args.get('text')
	if not text:
		return error()
	return process_page(text, request.args)

@route_page
def url():
	url = request.args.get('url')
	if not url:
		return error()

	# open and parse the website
	html = urllib.request.urlopen(url)
	soup = BeautifulSoup(html, 'html.parser').find('html')

	# remove unnecessary elements
	for group in ['head', 'script', 'style']:
		for elem in soup.findAll(group):
			elem.extract()

	# extract text from the page
	text = soup.findAll(text=True)

	return process_page(text, request.args)

@route_page
def author():
	author = request.args.get('author')
	if not author:
		return error()
	return process_page(pubmed_query(term='%s[Author]' % (author)), request.args)

@route_page
def pubmed():
	keyword = request.args.get('keyword')
	if not keyword:
		return error()
	return process_page(pubmed_query(term=keyword), request.args)

	# todo: get pubmed IDs from bmc page
	# we might need to be logged in for this to work
	pass
