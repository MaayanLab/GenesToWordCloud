from io import BytesIO
from flask import send_file
from wordcloud import WordCloud

def generate(text, stop_words=[]):
	""" Given any text, this function generates a word cloud """
	img = BytesIO()
	WordCloud().generate(text).to_image().save(img, 'jpeg')
	img.seek(0)
	return send_file(img, mimetype='image/jpg')
