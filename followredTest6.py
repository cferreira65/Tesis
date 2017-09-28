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


ids_opos = ids_opos.append(ids2, ignore_index=True)
ids_opos = ids_opos.append(ids3, ignore_index=True)
ids_opos = ids_opos.append(ids4, ignore_index=True)
ids_opos = ids_opos.append(ids5, ignore_index=True)
ids_opos = ids_opos.append(ids6, ignore_index=True)
ids_opos = ids_opos.append(ids7, ignore_index=True)
ids_opos = ids_opos.append(ids8, ignore_index=True)
ids_opos = ids_opos.append(ids9, ignore_index=True)
ids_opos = ids_opos.append(ids10, ignore_index=True)
ids_opos = ids_opos.append(ids11, ignore_index=True)
ids_opos = ids_opos.append(ids12, ignore_index=True)
ids_opos = ids_opos.append(ids13, ignore_index=True)

ids_chav = ids_chav.append(ids15, ignore_index=True)
ids_chav = ids_chav.append(ids16, ignore_index=True)
ids_chav = ids_chav.append(ids17, ignore_index=True)


ids_opos = pd.Series(ids_opos.unique())
ids_chav = pd.Series(ids_chav.unique())

print(ids_opos.size)
print(ids_chav.size)

CONSUMER_KEY = 'AhRlKdBDf2S8bYm0Euz4YgGge'
CONSUMER_SECRET = 'jr8XNDSK6WMkwBTULlP7JKdKe7LqoOHU13wNo9jHZM5bsA9jiG'
ACCESS_KEY = '86460420-HZLe5PlCwBzQjAPaOL8stIMezSD5xUrhn6nXK7GTy'
ACCESS_SECRET = 'DCFYG81MnxgrRi9wkPASUpGKaVvFdaU4jmlvqu0LHLz3m'
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
for user in ids_opos:
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
for user in ids_chav:
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
for user in ids_opos[3733:4066]:
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
        # print g_all.edges()
        print i
    except Exception, e:
        print(user)

for user in ids_chav[0:0]:
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
        # print g_all.edges()
        print i
    except Exception, e:
        print(user)

nx.write_graphml(g_all,'follow_all_3733-4066.xml')
nx.write_graphml(g_opos,'follow_opos_3733-4066.xml')
nx.write_graphml(g_chav,'follow_chav_3733-4066.xml')

