'''
Inform flask of the different pages available and do some basic preparation for process.py
'''

import urllib
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request
from process import process_page, error
from pubmed import pubmed_query
from config import config
from database import tables

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
	''' Database lookup for gene names '''
	genes = request.args.get('genes')
	if not genes:
		return error()
	genes = genes.split()

	source = request.args.get('source')
	if not source:
		return error()

	table = tables.get(source)
	if not table:
		return error()

	return process_page(list(table(genes)), request.args)

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
