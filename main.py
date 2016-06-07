#!/usr/local/bin/python3

from flask import Flask, render_template, url_for
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/create/genes')
def create_genes():
	return render_template('create/genes.html')

@app.route('/create/free_text')
def create_free_text():
	return render_template('create/free_text.html')

@app.route('/create/url')
def create_url():
	return render_template('create/url.html')

@app.route('/create/author')
def create_author():
	return render_template('create/author.html')

@app.route('/create/pubmed')
def create_pubmed():
	return render_template('create/pubmed.html')

@app.route('/create/bmc')
def create_bmc():
	return render_template('create/bmc.html')

@app.route('/view')
def view():
	return render_template('view.html')

@app.route('/help')
def help():
	return render_template('help.html')

app.run(debug=True)
