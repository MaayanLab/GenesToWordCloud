#!/bin/python3

from flask import Flask, render_template, url_for
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/create')
def create():
	return render_template('create.html')

@app.route('/view')
def view():
	return render_template('view.html')

@app.route('/help')
def help():
	return render_template('help.html')

app.run(debug=True)
