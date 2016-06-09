import re
import json
from io import BytesIO
from flask import send_file
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from config import config

def process_text(text, strip_symbols=True, tokenize=None, stemmer=None, lemmantize=None, case=None, stopwords=[], **kwargs):
	''' Process text pipeline, accepts different nlp flags
	tokenize, stemmer, lemmantize '''
	# https://github.com/wangz10/text-classification/blob/master/Main.ipynb

	if tokenize or type(text) == str:
		tokenizer = RegexpTokenizer(r'\b\w{1,}\b')
		words = tokenizer.tokenize(text)
	else:
		words = text

	if strip_symbols:
		words = list(filter(None, [re.sub(r'[^\w]','',word).strip() for word in words]))

	if case:
		words = list(
			map({
				'lower': str.lower,
				'upper': str.upper,
				'first': str.capitalize,
			}.get(case), words))

	if stemmer:
		stemmer = PorterStemmer()
		words = stemmer.stem(words)

	if lemmantize:
		lmmr = WordNetLemmatizer()
		words = lmmr.lemmantize(words)

	return [word for word in words
			if word not in stopwords]

def process_page(text, args):
	stopwords = []
	if args.get('stopwords'):
		stopwords += ENGLISH_STOP_WORDS
	if args.get('biostopwords'):
		stopwords += open('static/biostopwords.txt', 'r').readlines()
	if args.get('blacklist'):
		stopwords += args[blacklist].split()

	return json.dumps(
		process_text(text,
			stopwords=stopwords,
			case=args.get('case')))

def error():
	return json.dumps([])
