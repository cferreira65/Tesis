#!/usr/bin/env python

import sys
import string
import simplejson
import pandas as pd
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import botometer
import networkx as nx

df1 = pd.read_csv('Tweets/sosvenezuela_17-01.csv', sep= ';')
df2 = pd.read_csv('Tweets/sosvenezuela_17-02.csv', sep= ';')
df3 = pd.read_csv('Tweets/sosvenezuela_17-03.csv', sep= ';')
df4 = pd.read_csv('Tweets/sosvenezuela_17-04.csv', sep= ';')
df5 = pd.read_csv('Tweets/sosvenezuela_17-05.csv', sep= ';')

ids = df1.username #you can also use df['column_name']
# ids2 = df2.username
# ids3 = df3.username
# ids4 = df4.username
# ids5 = df5.username

# ids = ids.append(ids2, ignore_index=True)
# ids = ids.append(ids3, ignore_index=True)
# ids = ids.append(ids4, ignore_index=True)
# ids = ids.append(ids5, ignore_index=True)

ids = pd.Series(ids.unique())

ids = ids.sample(50)

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
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitterStream = Stream(auth,TweetListener())
desc = []

out = open("follow.txt", 'w')

g=nx.DiGraph()

i = 1
for user in ids:
    try:
        user_a = api.get_user(screen_name = user)
        desc.append(user_a)
        g.add_node(user)
        print i
        i = i + 1
    except Exception, e:
        print(user)

for user in ids:
#     #print user
    try:
        #desc.append(info.description)
        user_b_followers = tweepy.Cursor(api.followers_ids, id = user)
        i = 1
        for page in user_b_followers.pages():
            print i
            i = i + 1
            for user2 in desc:
                try:
                    is_following = user2.id in page    
                    if is_following:
                        g.add_edge(user2.screen_name,user)
                except Exception, e:
                    print ("user2 ", user2)
        print g.edges()
        print g.nodes()
    except Exception, e:
        print(user)
nx.write_graphml(g,'follow.xml')

out.close()
