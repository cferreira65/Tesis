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

df1 = pd.read_csv('test1.csv', sep= ';')
df2 = pd.read_csv('test2.csv', sep= ';')

# ids = df1.username #you can also use df['column_name']
# ids2 = df2.username
ids_opos = df1.username 
#ids4 = df4.username
# ids5 = df5.username
#ids6 = df6.username
#ids7 = df7.username
#ids8 = df8.username
# ids9 = df9.username
# ids10 = df10.username
#ids11 = df11.username
#ids12 = df12.username
#ids13 = df13.username
ids_chav = df2.username

# ids = ids.append(ids2, ignore_index=True)
# ids = ids.append(ids3, ignore_index=True)
#ids_opos = ids_opos.append(ids4, ignore_index=True)
# ids = ids.append(ids5, ignore_index=True)
#ids_opos = ids_opos.append(ids6, ignore_index=True)
#ids_opos = ids_opos.append(ids7, ignore_index=True)
#ids_opos = ids_opos.append(ids8, ignore_index=True)
# ids = ids.append(ids9, ignore_index=True)
# ids = ids.append(ids10, ignore_index=True)
#ids_opos = ids_opos.append(ids11, ignore_index=True)
#ids_opos = ids_opos.append(ids12, ignore_index=True)
#ids_opos = ids_opos.append(ids13, ignore_index=True)

ids_opos = pd.Series(ids_opos.unique())
ids_chav = pd.Series(ids_chav.unique())

print(ids_opos.size)
print(ids_chav.size)

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
desc_opos = []
desc_chav = []

g_all = nx.DiGraph()
g_opos = nx.DiGraph()
g_chav = nx.DiGraph()

i = 1
for user in ids_opos[0:10]:
    try:
        user_a = api.get_user(screen_name = user)
        desc_opos.append(user_a)
        g_all.add_node(user)
        g_opos.add_node(user)
        print i
        i = i + 1
    except Exception, e:
        print(user)

i = 1
for user in ids_chav[0:10]:
    try:
        user_a = api.get_user(screen_name = user)
        desc_chav.append(user_a)
        g_all.add_node(user)
        g_chav.add_node(user)
        print i
        i = i + 1
    except Exception, e:
        print(user)

i = 0
# usuarios de los hashtags opositores
for user in ids_opos[0:10]:
#     #print user
    i = i + 1
    try:
        #desc.append(info.description)
        user_b_followers = tweepy.Cursor(api.followers_ids, id = user)
        for page in user_b_followers.pages():
            #verificar que sigue a alguien de la lista de opositores
            for user2 in desc_opos:
                try:
                    is_following = user2.id in page    
                    if is_following:
                        g_all.add_edge(user2.screen_name,user)
                        g_opos.add_edge(user2.screen_name,user)
                except Exception, e:
                    print ("user2 ", user2)
            # verificar que sigue a alguien de la lista chavista
            for user2 in desc_chav:
                try:
                    is_following = user2.id in page    
                    if is_following:
                        g_all.add_edge(user2.screen_name,user)
                except Exception, e:
                    print ("user2 ", user2)
        print g_all.edges()
        print i
    except Exception, e:
        print(user)

for user in ids_chav[0:10]:
#     #print user
    i = i + 1
    try:
        #desc.append(info.description)
        user_b_followers = tweepy.Cursor(api.followers_ids, id = user)
        for page in user_b_followers.pages():
            #verificar que sigue a alguien de la lista de chavista
            for user2 in desc_chav:
                try:
                    is_following = user2.id in page    
                    if is_following:
                        g_all.add_edge(user2.screen_name,user)
                        g_chav.add_edge(user2.screen_name,user)
                except Exception, e:
                    print ("user2 ", user2)
            # verificar que sigue a alguien de la lista de opositores
            for user2 in desc_opos:
                try:
                    is_following = user2.id in page    
                    if is_following:
                        g_all.add_edge(user2.screen_name,user)
                except Exception, e:
                    print ("user2 ", user2)
        print g_all.edges()
        print i
    except Exception, e:
        print(user)

nx.write_graphml(g_all,'follow_all.xml')
nx.write_graphml(g_opos,'follow_opos.xml')
nx.write_graphml(g_chav,'follow_chav.xml')

