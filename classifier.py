#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import pandas as pd
import tweepy
import simplejson
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from array import array

df1 = pd.read_csv('users_opos_test.csv', sep= ',')
# df2 = pd.read_csv('no_bots_1000-2000.csv', sep= ';')

target = array('i')
data = []

user = df1.user
target_dictionary = {'Chavista': 1, 'Opositor': 2, 'Ninguno':3}

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
for u in user[:10]:
    try:
        classification = target_dictionary[df1.carlos[i]]
        i = i + 1
        user_object = api.get_user(screen_name = u) 
        description = user_object.description
        timeline = api.user_timeline(screen_name = u)
        data.append(description)
        target.append(classification)
        for tweet in timeline:
            data.append(tweet.text)
            target.append(classification)
    except Exception, e:
        print(u)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(data)
print(X_train_counts.shape)
print(count_vect.vocabulary_.get(u'sigue'))
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print(X_train_tfidf.shape)

print(len(data))
print(len(target))

