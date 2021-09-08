from api_call import *
from database_mongo import *
import time
import json

def clear_search():
	listOfGlobals = globals()
	listOfGlobals['outcome'] = {}
	listOfGlobals['new_list'] = [[],[],[],[]]
	listOfGlobals['total_ans'] =[]
	listOfGlobals['ans'] =[]
	listOfGlobals['temp_level'] =[]
	listOfGlobals['total_list'] =[]
	



def scoring(article):
	score = 0
	outcome[json.dumps(article)] = 0
	tokens = word_tokenize(article['Content_lower'])
	temp_total_ans = total_ans.copy()
	for word in article['Keywords']:
		if word in new_list[0] or word in new_list[1]:
			score+=10
			temp_total_ans.remove(word)

	for word in tokens:
		points = 2
		if word in temp_total_ans:
			if word in new_list[1]:
				points/=2
			elif word in new_list[2]:
				points/=4
			elif word in new_list[3]:
				points/=8
			score+=points

	if score>0:
		outcome[json.dumps(article)] += score
	else:
		outcome.pop(json.dumps(article), None)

# global variables
outcome = {}
new_list = [[],[],[],[]]
total_ans =[]
ans = []

def main(sentence,page):
	global new_list
	global total_ans
	global outcome
	start = time.time()
	if page==0:
		outcome = {}
		new_list = [[],[],[],[]]
		total_ans =[]
		ans = []
		x = get_tokens(sentence.strip())
		ans,total_ans = get_tree(x)
		for i in ans:
			new_list[0]=i[0]
			new_list[1]=i[1]
			new_list[2]=i[2]
			new_list[3]=i[3]

	for level in new_list:
		print(level)

	articles = content_multiple_keyword(total_ans,page)

	pool = ThreadPool(20)
	pool.map(scoring, articles)

	outcome = dict(sorted(outcome.items(), key=lambda item: item[1]))

	data = []
	for i in outcome:
		score = (outcome[i])
		temp = json.loads(i)
		temp['score'] = score
		data.append(temp)

	data = data[::-1]
	end = time.time()
	print(end-start)

	listOfGlobals = globals()
	listOfGlobals['outcome'] = {}

	print(len(data))
	return data