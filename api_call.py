# make an api call and then just get the data from the user and start scoring
# create an inverse tfidf score and then get the data of the user from that and then run the query
# give scores to each article and then sort them in desc order and output the result

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

import requests 
from bs4 import BeautifulSoup
import json

from multiprocessing.dummy import Pool as ThreadPool


#  REMOVING PUNCTUATIONS AFTER TOKENISATION
def get_tokens(sentence):

	punctuations = nltk.RegexpTokenizer(r"\w+")
	tokenized_sen = punctuations.tokenize(sentence)

	# LEMMATIZE
	lemm = WordNetLemmatizer()
	x = []
	for i in tokenized_sen:
		x.append(lemm.lemmatize(i))

	# STOP WORDS
	x1 = []
	stop_words = stopwords.words('english')
	for i in x:
		if i not in stop_words:
			x1.append(i)
	return x1


def get_syn(word):
	url1="https://www.wordsapi.com/mashape/words/"
	url2="/synonyms?when=2021-06-09T17:09:42.975Z&encrypted=8cfdb18be722959bea9807bee858beb0aeb42f0939f892b8"
	request_api = requests.get(url1+word+url2)
	text = request_api.text
	soup = BeautifulSoup(text, 'lxml')
	words = soup.find("p").getText()
	data = json.loads(words)
	syn = data.get("synonyms")
	if syn==None:
		return
	if(len(syn)!=0):
		# only taking the top 10 syn as we dont want to make a word clutter
		for w in syn[:5]:
			if w not in total_list and len(w.split(" "))==1:
				temp_level.append(w)
				total_list.append(w)
	return


# globals=
temp_level = []
total_list = []

def get_tree(words):
	global temp_level
	global total_list

	l2 = []
	l3 = []
	l4 = []
	ans = []
	total_ans = set()
	total_list = []
	final_tree = []
	temp_level = []

	# level 1
	l1 = words
	final_tree.append(l1)
	for word in words:
		total_list.append(word)

	# level 2
	pool = ThreadPool(10)
	pool.map(get_syn, l1)
	l2 = [x for x in temp_level]
	final_tree.append(temp_level)
	temp_level = []
	
	# level 3
	pool = ThreadPool(10)
	pool.map(get_syn, l2)
	l3 = [x for x in temp_level]
	final_tree.append(temp_level)
	temp_level = []

	# level 4
	pool = ThreadPool(10)
	pool.map(get_syn, l3)
	l4 = [x for x in temp_level]
	final_tree.append(temp_level)
 
	ans.append(final_tree)

	for i in total_list:
		total_ans.add(i)

	return ans,list(total_ans)

if __name__ == "__main__":
	sentence = input("enter sentence -> ")
	x = get_tokens(sentence)

	ans,total_ans = get_tree(x)

	print(ans)
	print(len(total_ans))