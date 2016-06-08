from io import BytesIO
from flask import send_file
from wordcloud import WordCloud
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from config import config

def process_text(text, **kwargs):
	# https://github.com/wangz10/text-classification/blob/master/Main.ipynb

	if kwargs.get('tokenize'):
		tokenizer = RegexpTokenizer(r'\b\w{1,}\b')
		words = tokenizer.tokenize(text)
	else:
		words = text

	if kwargs.get('stemmer'):
		stemmer = PorterStemmer()
		words = stemmer.stem(words)

	if kwargs.get('lemmantize'):
		lmmr = WordNetLemmatizer()
		words = lmmr.lemmantize(words)

	return ' '.join(words)

def generate(text, **kwargs):
	img = BytesIO()
	WordCloud(**kwargs).generate(text).to_image().save(img, 'jpeg')
	img.seek(0)
	return send_file(img, mimetype='image/jpg')


def process_page(text, args):
	g = {'stopwords': []}
	p = {}

	stopwords = args.get('stopwords')
	if stopwords:
		g['stopwords'] += ENGLISH_STOP_WORDS

	biostopwords = args.get('biostopwords')
	if biostopwords:
		g['stopwords'] += open('static/biostopwords.txt', 'r').readlines()

	angler = args.get('angler')
	if angler:
		if angler == 'mostlyHoriz':
			g['prefer_horizontal'] = 0.9
		elif angler == 'horiz':
			g['prefer_horizontal'] = 1.0
		elif angler == 'random':
			g['prefer_horizontal'] = random.uniform(0, 1)
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
		g['stopwords'] += blacklist.split()

	g['width'], g['height'] = min(config['word_cloud']['max_width'], int(args.get('width'))), min(config['word_cloud']['max_height'], int(args.get('height')))

	return generate(process_text(text, **p), **d)
