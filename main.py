#!/usr/local/bin/python3

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
	app.add_url_rule('/view/%s' % (name), 'view_%s' % (name), func, methods=['POST'])

@route_page
def genes():
	return render_template('view/genes.html',
		genes=request.form['genes'],
		source=request.form['source'])

@route_page
def free_text():
	return render_template('view/free_text.html',
		text=request.form['text'],
		stopwords=request.form['stopwords'],
		biostopwords=request.form['biostopwords'])

@route_page
def url():
	return render_template('view/url.html')

@route_page
def author():
	return render_template('view/author.html')

@route_page
def pubmed():
	return render_template('view/pubmed.html')

@route_page
def bmc():
	return render_template('view/bmc.html')


app.run(debug=True)
