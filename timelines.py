#!/usr/bin/env python

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

opos = df1.User #you can also use df['column_name']
chav = df2.User

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

def quit_character(character, text):
    new_text = ""
    for i in text.replace('\n','').encode('utf-8'):
        new_text =  new_text + i.strip(character)

    return "\"" + new_text + "\""

#search
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitterStream = Stream(auth,TweetListener())
opos_timeline = []
chav_timeline = []

op = []
ch = []


for user in opos:
    try:
        user_a = api.user_timeline(screen_name = user)
        opos_timeline.append(user_a)
        op.append(user)
    except Exception, e:
        print(user)
        print(e)

out1 = open("oposTimelineText.csv", 'w')

i = 0
for user in op:
    out1.write(user + ";")
    for tw in opos_timeline[i]:
        out1.write(quit_character(';', tw.text))
        out1.write(";")
    out1.write("\n")
    i = i + 1

for user in chav:
    try:
        user_a = api.user_timeline(screen_name = user)
        chav_timeline.append(user_a)
        ch.append(user)
    except Exception, e:
        print(user)
        print(e)
        chav.drop(chav.index[i])

out2 = open("chavTimelineText.csv", 'w')

i = 0
for user in ch:
    out2.write(user + ";")
    for tw in chav_timeline[i]:
        out2.write(quit_character(';', tw.text))
        out2.write(";")
    out2.write("\n")
    i = i+1

