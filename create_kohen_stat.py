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

df1 = pd.read_csv('users_clasificados/users_opos_final.csv', sep= ',')
df2 = pd.read_csv('users_clasificados/users_chav_final.csv', sep= ',')

opos = df1.User
chav = df2.User

carlos1 = df1.Clasificador1
carlos2 = df2.Clasificador1

dayana1 = df1.Clasificador2
dayana2 = df2.Clasificador2

andres1 = df1.Clasificador3
andres2 = df2.Clasificador3

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
out = open("users_clasificados/all_users.csv", 'w')

out.write("User,Link,Clasificador1,Clasificador2,Clasificador3\n")

i = 0
for user in opos:
    try:
        user_a = api.user_timeline(screen_name = user)
        # desc_chav.append(user_a)
        out.write(user + ",https://twitter.com/" + user + "," + carlos1[i] + "," + dayana1[i] + "," + andres1[i] + "\n")
        i = i + 1
    except Exception, e:
        print(user)
        i = i + 1

i = 0
for user in chav:
    try:
        user_a = api.user_timeline(screen_name = user)
        # desc_chav.append(user_a)
        out.write(user + ",https://twitter.com/" + user + "," + carlos2[i] + "," + dayana2[i] + "," + andres2[i] + "\n")
        i = i + 1
    except Exception, e:
        print(user)
        i = i + 1

out.close()