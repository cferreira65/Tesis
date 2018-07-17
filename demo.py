#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import string
import random
import pandas as pd
import numpy as np
from array import array
import simplejson
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords




class TweetListener(StreamListener):
	# A listener handles tweets are the received from the stream.
	#This is a basic listener that just prints received tweets to standard output

	def on_data(self, data):
		print data
		return True

	def on_error(self, status):
		print status

def quit_character(character, text):
	new_text = ""
	for i in text.replace('\n','').encode('utf-8'):
		new_text =  new_text + i.strip(character)

	return new_text 

#search

def getTimeline(user):

	api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	twitterStream = Stream(auth,TweetListener())
	timeline = []

	out1 = open("demo/timeline.csv", 'w')

	i = 0

	try:
		user_object = api.get_user(screen_name = user)
		timeline = api.user_timeline(screen_name = user)
		out1.write(user + ";")
		out1.write(quit_character(';', user_object.description))
		out1.write(";")

		for tw in timeline:
			out1.write(quit_character(';', tw.text))
			out1.write(";")

		out1.write("\n")

	except Exception, e:
		print(user)
		print(e)

	out1.close()



def clean_demo_stopwords():

	data = []
	fp = open('demo/timeline.csv', 'r')
	line = fp.readline()
	out = open("demo/stopwords.txt", 'w')

	while line:
		#data.append(line.split(';'))
		#line = fp.readline()

		data = line.split(';')
		# stop words
		train_data = ""
		out.write(data[0])
		out.write(";")
		for d in data[1:-1]:
			d = d.lower()
			filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
			filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
			train_data = ' '.join(word for word in filtered_words)
			out.write(train_data)
			out.write(";")
		
		out.write(data[-1])     
		line = fp.readline()


	fp.close
	out.close


def result(lis):
		count = [0,0]

		for prediction in lis:
			count[prediction] = count[prediction] + 1

		if (count[0] == count[1]):
			res = random.randint(0,1)
		elif (count[0] > count[1]):
			res = 0
		elif (count[1] > count[0]):
			res = 1
		else:
			res = random.randint(0,1)
		return res

# CONJUNTO DE ENTRENAMIENTO

def train():

	random.seed(42)

	target_dictionary = {'Chavista\n': 0, 'Oposición\n': 1, 'Ninguno\n':2}

	target = array('i')
	fp = open('stopwords/opos_stopwords.txt', 'r')
	line = fp.readline()
	fp2 = open('stopwords/chav_stopwords.txt', 'r')
	fp3 = open('demo/stopwords.txt', 'r')

	print("A")

	while line:

		data = line.split(';')
		if target_dictionary[data[-1]] != 2:
			user.append(data[1:-1])
			clas.append(target_dictionary[data[-1]])
		line = fp.readline()

	line = fp2.readline()

	print("B")

	while line:

		data = line.split(';')
		if target_dictionary[data[-1]] != 2:
			user.append(data[1:-1])
			clas.append(target_dictionary[data[-1]])
		line = fp2.readline()

	
	print("C")

	line = fp3.readline()
	data = line.split(';')
	text_user.append(data[1:-1])

	fp.close
	fp2.close
	fp3.close

	i = 0
	target = array('i')
	print("D")
	# print(clas)
	for t in user:
		for d in user[i]:
			train_data.append(d)
			target.append(clas[i])
		i = i + 1


	statistic = [[], [], []]

	#count_vect= CountVectorizer(ngram_range = (1,2))

	X_train_counts = count_vect.fit_transform(train_data)
	

	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

	print("E")

	SGD = SGDClassifier(loss='hinge', penalty='l2',
							alpha=1e-3, random_state=42,
							max_iter=5, tol=None).fit(X_train_counts, target)

	return SGD	
		

def predict(trained):

	prediction = []

	test_clasification = []

	test_data = []

	
	for d in text_user[0]:

		test_data.append(d)

		X_new_counts = count_vect.transform(test_data)        

		X_new_tfidf= tfidf_transformer.transform(X_new_counts)

		predicted = trained.predict(X_new_tfidf)


		res = result(predicted)
		prediction.append(res)   

	
	print(prediction)

	# string = "demo/resultados.txt"
	# out = open(string, 'w')


	# out.write("Estadisticas:\n")

	# out.write(str(metrics.classification_report(test_clasification, prediction,
	# 				target_names=["Chavista","Opositor"])))

	# out.write(str(metrics.confusion_matrix(test_clasification, prediction)))

	# out.write("\n")

	# statistic[0].append(res[0])
	# statistic[1].append(res[1])
	# statistic[2].append(res[2])

	# out = open("demo/resultados", 'w')

	# out.write("Promedio:\n")
	# out.write("Precision: " + str(np.mean(statistic[0])) + "\n")
	# out.write("Recall: " + str(np.mean(statistic[1])) + "\n")
	# ut.write("Fscore: " + str(np.mean(statistic[2])) + "\n")


# OBTENCION DE DATOS TWITTER

CONSUMER_KEY = 'FUjJNyet2iQ3DrmSs8zdclFgG'
CONSUMER_SECRET = '1l8uippLO9oeJS1b28aPwLqAizI6MkacUXofje6XMcEMEeVAwn'
ACCESS_KEY = '86460420-zaHoxJV9XSfxnppUTMlmMCtYDgFopK1yg4fiVGBet'
ACCESS_SECRET = '0uD03WJIlejK5K7YemoSMpXJe4ujII0RfJuERMoiEDLWu'
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.secure = True
api = tweepy.API(auth)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

data = []
user = []
text_user = []
clas = []
user_clas = []
train_data = []
user_test = []

count_vect= CountVectorizer(ngram_range = (1,2))
tfidf_transformer = TfidfTransformer()
print("Training, please wait...\n")

trained = train()

while True:
	print("Please enter the Twitter username:\n")
	username = raw_input()
	print("Searching the user info from Twitter...\n")
	getTimeline(username)
	clean_demo_stopwords()
	print("Prediction:\n")
	predict(trained)






