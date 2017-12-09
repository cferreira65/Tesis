#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import pandas as pd
import tweepy
import simplejson
import numpy as np
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from array import array


df1 = pd.read_csv('users_opos_test.csv', sep= ',')
# df2 = pd.read_csv('no_bots_1000-2000.csv', sep= ';')

target = array('i')
train_data = []

user = df1.user
target_dictionary = {'Chavista': 0, 'Opositor': 1, 'Ninguno':2}

CONSUMER_KEY = 'FUjJNyet2iQ3DrmSs8zdclFgG'
CONSUMER_SECRET = '1l8uippLO9oeJS1b28aPwLqAizI6MkacUXofje6XMcEMEeVAwn'
ACCESS_KEY = '86460420-zaHoxJV9XSfxnppUTMlmMCtYDgFopK1yg4fiVGBet'
ACCESS_SECRET = '0uD03WJIlejK5K7YemoSMpXJe4ujII0RfJuERMoiEDLWu'
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.secure = True
api = tweepy.API(auth)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

#search
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitterStream = Stream(auth,TweetListener())

i = 0
for u in user[:9]:
    try:
        classification = target_dictionary[df1.carlos[i]]
        i = i + 1
        user_object = api.get_user(screen_name = u) 
        description = user_object.description
        timeline = api.user_timeline(screen_name = u)
        train_data.append(description)
        target.append(classification)
        for tweet in timeline:
            train_data.append(tweet.text)
            target.append(classification)
    except Exception, e:
        print(u)

# text_clf = Pipeline([('vect', CountVectorizer()),
#                     ('tfidf', TfidfTransformer()),
#                     ('clf', MultinomialNB()),
# ])

# text_clf.fit(train_data, target)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train_data)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, target)
clf2 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=5, tol=None).fit(X_train_tfidf, target)

# print(X_train_counts.shape)
# print(count_vect.vocabulary_.get(u'sigue'))
# print(X_train_tfidf.shape)


for u in user[9:10]:
    try:
        test_data = []
        result = [0,0,0]
        classification = target_dictionary[df1.carlos[i]]
        i = i + 1
        user_object = api.get_user(screen_name = u) 
        description = user_object.description
        timeline = api.user_timeline(screen_name = u)
        test_data.append(description)
        # target.append(classification)
        for tweet in timeline:
            test_data.append(tweet.text)
            # target.append(classification)
        X_new_counts = count_vect.transform(test_data)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        predictedNB = clf.predict(X_new_tfidf)
        # predicted = text_clf.predict(test_data)
        predictedSGD = clf2.predict(X_new_tfidf)

        for prediction in predictedNB:
            result[prediction] = result[prediction] + 1

        if (result[0] == result[1]):
            res = "Ninguno"
        elif (result[0] > result[1] and result[0] > result[2]):
            res = "Chavista"
        elif (result[1] > result[0] and result[1] > result[2]):
            res = "Opositor"
        else:
            res = "Chavista"
        print("La predicción de NB es: " + res)
        
        result = [0,0,0]
        for prediction in predictedSGD:
            result[prediction] = result[prediction] + 1

        if (result[0] == result[1]):
            res = "Ninguno"
        elif (result[0] > result[1] and result[0] > result[2]):
            res = "Chavista"
        elif (result[1] > result[0] and result[1] > result[2]):
            res = "Opositor"
        else:
            res = "Chavista"
        print("La predicción de SGD es: " + res)


    except Exception, e:
        print(u)


print(test_data)
print(predictedNB)
print(predictedSGD)

# print(predicted)

print(len(train_data))
print(len(target))

