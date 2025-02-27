'''
Process functions for analyzing the text, processing it, and returning a json with the results
'''

import re
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

def tokenize_text(text):
	tokenizer = RegexpTokenizer(r'\b\w{2,}\b')
	return tokenizer.tokenize(text.lower())

def strip_text(words):
	for word in words:
		w = re.sub(r'[^\w]','',word).strip()
		if w:
			try: # Remove pure numbers
				int(w)
			except:
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
	m, s = r.mean(), r.std()
	return sorted(
		[[str(word), float((r[ind] - m) / s)]
		 for word, ind in cv.vocabulary_.items()],
		 key=lambda p: p[1], reverse=True)

def process_page(text, args):
	''' Take text from app.py and GET args and feed it through processing steps '''
	stopwords = []
	if args.get('stopwords'):
		stopwords += map(str.strip, open('static/stopwords.txt', 'r').readlines())
	if args.get('biostopwords'):
		stopwords += map(str.strip, open('static/biostopwords.txt', 'r').readlines())
	if args.get('customstopwords'):
		stopwords += map(str.strip, args['customstopwords'].split())
	return json.dumps(process_text(text, stop_words=stopwords))

def error():
	return "[]"
