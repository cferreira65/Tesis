#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import simplejson
import random
import pandas as pd
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

df1 = pd.read_csv('users_opos_test.csv', sep= ',')
df2 = pd.read_csv('users_chav_test.csv', sep= ',')
df14 = pd.read_csv('archivos_corridas/no_bots_15335-16835.csv', sep= ';')
df15 = pd.read_csv('archivos_corridas/no_bots_16835-18335.csv', sep= ';')
df16 = pd.read_csv('archivos_corridas/no_bots_18335-19804.csv', sep= ';')

chav = df2.User

ids_chav = df14.username
ids15 = df15.username
ids16 = df16.username

ids_chav = ids_chav.append(ids15)
ids_chav = ids_chav.append(ids16)
ids_chav = pd.Series(ids_chav.unique())

user_chav = ids_chav.sample(n=100)

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


api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitterStream = Stream(auth,TweetListener())
out2 = open("chav_faltantes.csv", 'w')

for user in user_chav:
    try:
        user_a = api.user_timeline(screen_name = user)
        # desc_chav.append(user_a)
        if not(user in chav.unique()):
        	out2.write(user + ", https://twitter.com/" + user + "\n")
        i = i + 1
    except Exception, e:
        print(user)

out2.close()