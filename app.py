import re
import urllib
import random
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
		return render_template('create/%s.html' % (name), cloud_type=name)
	app.add_url_rule('/create/%s' % (name), 'create_%s' % (name), create)
	app.add_url_rule('/view/%s' % (name), 'view_%s' % (name), func, methods=['GET'])

def process_page(text, args):
	d = {}

	angler = args.get('angler')
	if angler:
		if angler == 'mostlyHoriz':
			d['prefer_horizontal'] = 0.9
		elif angler == 'horiz':
			d['prefer_horizontal'] = 1.0
		elif angler == 'random':
			d['prefer_horizontal'] = random.uniform(0, 1)
	# todo: heaped, hexes

	placer = args.get('placer')
	if placer:
		pass
		# centerClump, horizBandAnchoredLeft, horizLine, swirl, upperLeft, wave

	case = args.get('case')
	if case:
		if case == 'lower':
			text = text.lower()
		elif case == 'upper':
			text = text.upper()
		elif case == 'first':
			text = text.capitalize()

	blacklist = args.get('blacklist')
	if blacklist:
		d['stopwords'] = blacklist.split()

	d['width'], d['height'] = min(1920, int(args.get('width'))), min(1200, int(args.get('height')))

	return generate(text, **d)

@route_page
def genes():
	# request.form['genes']
	# request.form['source']
	pass

@route_page
def free_text():
	text = request.args.get('text')
	if not text:
		return None
	# todo stopwords, biostopwords
	return process_page(text, request.args)

@route_page
def url():
	url = urllib.request.urlopen(request.args.get('url'))
	text = '\n'.join(map(str, url.readlines()))
	url.close()
	# todo: stopwords, biostopwords
	return process_page(text, request.args)

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
