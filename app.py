import urllib
import pyodbc
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request
from word_cloud import process_page
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
	gene_query = ' or '.join(['geneName="%s"' % (gene) for gene in genes.split()])

	source = request.args.get('source')
	if not source:
		return None

	con = pyodbc.connect(config['database'])
	with con.cursor() as cur:
		if source == "generif":
			cur.execute('select generif, pmid from generif where ? order by random(), pmid limit ?', (gene_query, config['query_limit']))
			text = [pubmed_query(id=row['pmid']) for row in cur.fetchall()]
		elif source == 'pubmed':
			cur.execute('select pmid from pmid_symbol where ? order by random() limit ?', (gene_query, config['query_limit']))
			text = [pubmed_query(id=row['pmid']) for row in cur.fetchall()]
		elif source == 'go':
			cur.execute('select go, goID from go where ? order by random(), goID limit ?', (gene_query, config['query_limit']))
			text = [row['go'] for row in cur.fetchall()]
		elif source == 'mp':
			cur.execute('select mp, mpID from mp where ? order by random(), mp limit ?', (gene_query, config['query_limit']))
			text = [row['mp'] for row in cur.fetchall()]
		elif source == 'mesh_terms':
			cur.execute('select pmid from pmid_symbol where ? order by random() limit ?', (gene_query, config['query_limit']))
			text = [pubmed_query(id=row['pmid']) for row in cur.fetchall()]
		else:
			return None
	con.close()

	return process_page(text, request.args)

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
	text = list(filter(None, map(str.strip, soup.findAll(text=True))))
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
