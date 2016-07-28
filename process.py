'''
Process functions for analyzing the text, processing it, and returning a json with the results
'''

import re
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from config import config

def tokenize_text(text):
	tokenizer = RegexpTokenizer(r'\b\w{1,}\b')
	return tokenizer.tokenize(text)

def strip_text(words):
	for word in words:
		w = re.sub(r'[^\w]','',word).strip()
		if w:
			yield(w)

def lemmatize_text(words):
	lmmr = WordNetLemmatizer()
	for word in words:
		yield(lmmr.lemmatize(word))

def preprocess_text(text):
	return lemmatize_text(strip_text(tokenize_text(text)))

def process_text(text, **kwargs):
	''' Count the word frequencies and return a dict of the results '''
	cv = CountVectorizer( # TfidfVectorizer
		min_df=1, max_df=100,
		analyzer='word',
		tokenizer=preprocess_text,
		strip_accents='unicode',
		**kwargs) #  ngram_range=(1,2),
	r = cv.fit_transform([text]).toarray()[0]
	return sorted(
		[[str(word), int(freq)]
		 for word, freq in zip(cv.vocabulary_.keys(), r)],
		 key=lambda p: p[1], reverse=True)

def process_page(text, args):
	''' Take text from app.py and GET args and feed it through processing steps '''
	stopwords = []
	if args.get('stopwords'):
		stopwords += map(str.strip, open('static/stopwords.txt', 'r').readlines())
	if args.get('biostopwords'):
		stopwords += map(str.strip, open('static/biostopwords.txt', 'r').readlines())
	if args.get('blacklist'):
		stopwords += map(str.strip, args['blacklist'].split())
	return json.dumps(process_text(text, stop_words=stopwords))

def error():
	return "[]"
