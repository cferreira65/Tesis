#!/usr/bin/env python

import sys
import string
import simplejson
import pandas as pd
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler


df = pd.read_csv('users.csv', sep= ';')

ids = df.username #you can also use df['column_name']
ids_s = []

for i in ids:
	ids_s.append(i.partition(' ')[0])

CONSUMER_KEY = '5Rcxy0B6hTefj4WfI83Ov4rGn'
CONSUMER_SECRET = 'IROZKaE6Osnt7FlvVmZlWLEU9V1KT7TyZpda7CgrJKG5Qmtre5'
ACCESS_KEY = '86460420-9xJaN64nnrumh3QRJEfKWhTFcjf572kOtHGbRMkta'
ACCESS_SECRET = 'Rarw3wksqYiVDZsTMPebWDztDSuQuXSiIwfz40jgMkrsC'
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
api = tweepy.API(auth)
twitterStream = Stream(auth,TweetListener())
desc = []

out = open("out.csv", 'w')

for user in ids_s:
	#print user
	info = api.get_user(screen_name = user)
	#desc.append(info.description)
	inf = info.description
	out.write(user + ",\"" + inf.rstrip("\n").encode('utf-8') + "\"\n")

'''dataf = pd.DataFrame(np.column_stack([ids_s, desc]), 
                               columns=['username', 'description'])
dataf.to_csv("out.csv", sep=';')'''
out.close()