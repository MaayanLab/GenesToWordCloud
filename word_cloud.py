from io import BytesIO
from flask import send_file
from wordcloud import WordCloud

def generate(text, **kwargs):
	""" Given any text, this function generates a word cloud """
	img = BytesIO()
	WordCloud(**kwargs).generate(text).to_image().save(img, 'jpeg')
	img.seek(0)
	return send_file(img, mimetype='image/jpg')
