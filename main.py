#!/usr/local/bin/python3

import re
import urllib 
from word_cloud import generate
from flask import Flask, render_template, url_for, request
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
		return render_template('create/%s.html' % (name))
	app.add_url_rule('/create/%s' % (name), 'create_%s' % (name), create)
	app.add_url_rule('/view/%s' % (name), 'view_%s' % (name), func, methods=['GET'])

@route_page
def genes():
	# request.form['genes']
	# request.form['source']
	pass

@route_page
def free_text():
	text = request.args.get('text')
	# request.form['stopwords'],
	# request.form['biostopwords'],
	return generate(text)

@route_page
def url():
	text = urllib.request.get(request.args.get('url')).text
	# html entities
	# request.form['stopwords'],
	# request.form['biostopwords'],
	return generate(text)

@route_page
def author():
	pass

@route_page
def pubmed():
	pass

@route_page
def bmc():
	if request.form['date'] == 'year':
		urllib.request.get('http://www.biomedcentral.com/bmcbioinformatics/mostviewedbyyear/')
	elif request.form['date'] == 'ever':
		urllib.request.get('http://www.biomedcentral.com/mostviewedalltime/')
	else:
		urllib.request.get('http://www.biomedcentral.com/bmcbioinformatics/mostviewed/')
	# todo
	pass


app.run(debug=True)
