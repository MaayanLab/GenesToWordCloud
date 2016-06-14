'''
Process functions for analyzing the text, processing it, and returning a json with the results
'''

import re
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from config import config

def preprocess_text(text, strip_symbols=True, tokenize=None, stemmer=None, lemmantize=None, case=None, **kwargs):
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

	return words

def process_text(text, stopwords=[], **kwargs):
	''' Count the word frequencies and return a dict of the results '''
	cv = CountVectorizer(min_df=1, max_df=100, analyzer='word', ngram_range=(1,2), stop_words=stopwords)
	r = cv.fit_transform([' '.join(text)]).toarray()[0]
	return [{'text': str(word), 'freq': int(freq)}
			 for word, freq in zip(cv.vocabulary_.keys(), r)]

def process_page(text, args):
	''' Take text from app.py and GET args and feed it through processing steps '''
	stopwords = []
	if args.get('stopwords'):
		stopwords += ENGLISH_STOP_WORDS
	if args.get('biostopwords'):
		stopwords += open('static/biostopwords.txt', 'r').readlines()
	if args.get('blacklist'):
		stopwords += args['blacklist'].split()
	return json.dumps(
		process_text(
			preprocess_text(text, case=args.get('case')),
			stopwords=stopwords))

def error():
	return "[]"
