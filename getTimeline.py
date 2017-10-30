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

df1 = pd.read_csv('no_bots_1-1000.csv', sep= ';')
df2 = pd.read_csv('no_bots_1000-2000.csv', sep= ';')
df3 = pd.read_csv('no_bots_2000-3000.csv', sep= ';')
df4 = pd.read_csv('no_bots_3000-4000.csv', sep= ';')
df5 = pd.read_csv('no_bots_4000-5500.csv', sep= ';')
df6 = pd.read_csv('no_bots_5500-7000.csv', sep= ';')
df7 = pd.read_csv('no_bots_7000-8500.csv', sep= ';')
df8 = pd.read_csv('no_bots_8500-10000.csv', sep= ';')
df9 = pd.read_csv('no_bots_10000-11500.csv', sep= ';')
df10 = pd.read_csv('no_bots_11500-13000.csv', sep= ';')
df11 = pd.read_csv('no_bots_13000-14200.csv', sep= ';')
df12 = pd.read_csv('no_bots_14200-15335.csv', sep= ';')
df13 = pd.read_csv('Tweets/selected_users_opos.csv', sep =';')

df14 = pd.read_csv('no_bots_15335-16835.csv', sep= ';')
df15 = pd.read_csv('no_bots_16835-18335.csv', sep= ';')
df16 = pd.read_csv('no_bots_18335-19804.csv', sep= ';')
df17 = pd.read_csv('Tweets/selected_users_chav.csv', sep =';')

ids_opos = df1.username #you can also use df['column_name']
ids2 = df2.username
ids3 = df3.username 
ids4 = df4.username
ids5 = df5.username
ids6 = df6.username
ids7 = df7.username
ids8 = df8.username
ids9 = df9.username
ids10 = df10.username
ids11 = df11.username
ids12 = df12.username
ids13 = df13.username
ids_chav = df14.username
ids15 = df15.username
ids16 = df16.username
ids17 = df17.username


ids_opos = ids_opos.append(ids2)
ids_opos = ids_opos.append(ids3)
ids_opos = ids_opos.append(ids4)
ids_opos = ids_opos.append(ids5)
ids_opos = ids_opos.append(ids6)
ids_opos = ids_opos.append(ids7)
ids_opos = ids_opos.append(ids8)
ids_opos = ids_opos.append(ids9)
ids_opos = ids_opos.append(ids10)
ids_opos = ids_opos.append(ids11)
ids_opos = ids_opos.append(ids12)
ids_opos = ids_opos.append(ids13)

ids_chav = ids_chav.append(ids15)
ids_chav = ids_chav.append(ids16)
ids_chav = ids_chav.append(ids17)

ids = ids_opos.append(ids_chav)

ids_opos = pd.Series(ids_opos.unique())
ids_chav = pd.Series(ids_chav.unique())
ids = pd.Series(ids.unique())

print(ids_opos.size)
print(ids_chav.size)

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
desc_opos = []
desc_chav = []

random.shuffle(ids)

i = 1
for user in ids[0:1000]:
    try:
        user_a = api.user_timeline(screen_name = user)
        desc_opos.append(user_a)
        print i
        i = i + 1
    except Exception, e:
        print(user)

i = 1
for user in ids[1000:2000]:
    try:
        user_a = api.user_timeline(screen_name = user)
        desc_chav.append(user_a)
        print i
        i = i + 1
    except Exception, e:
        print(user)

out1 = open("tweets-0-1000.csv", 'w')
out2 = open("tweets-1000-2000.csv", 'w')

i = 0
for user in desc_opos:
    out1.write(str(i))
    for u in user:
        out1.write(", https://twitter.com/dummyacc/status/" + u.id_str)
    out1.write("\n")
    i = i + 1

for user in desc_chav:
    out2.write(str(i))
    for u in user:
        out2.write(", https://twitter.com/dummyacc/status/" + u.id_str)
    out2.write("\n")
    i = i + 1

#https://twitter.com/statuses/ID