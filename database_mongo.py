import pymongo
from pymongo import MongoClient
import json

client = pymongo.MongoClient("mongodb+srv://tanishq:tanishq@live-stock.nyuyi.mongodb.net/Live-stock?retryWrites=true&w=majority")
db = client['SEO']
collection = db['Newspaper_Data']

def content_multiple_keyword(words,page):
	query = []
	article_dic = {}
	for word in words:
		word = "^"+word
		query.append({"Content_words":{'$regex': word}})
	articles = list(collection.find({'$or':query}, {'Article_id':0,'Content_words':0,'_id': 0}).skip(page*1000).limit(1000))
	return articles