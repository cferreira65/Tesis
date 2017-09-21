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

# All the files containing the tweets
df1 = pd.read_csv('Tweets/sosvenezuela_17-01.csv', sep= ';')
df2 = pd.read_csv('Tweets/sosvenezuela_17-02.csv', sep= ';')
df3 = pd.read_csv('Tweets/sosvenezuela_17-03.csv', sep= ';')
df4 = pd.read_csv('Tweets/sosvenezuela_17-04.csv', sep= ';')
df5 = pd.read_csv('Tweets/sosvenezuela_17-05.csv', sep= ';')
# -----------------------
df6 = pd.read_csv('Tweets/sosvenezuela_17-06.csv', sep= ';')
df7 = pd.read_csv('Tweets/sosvenezuela_17-07.csv', sep= ';')
# -----------------------
df8 = pd.read_csv('Tweets/ChavezVive15-04-17.csv', sep= ';')
# df7 = pd.read_csv('Tweets/ChavezVive15-08-13.csv', sep= ';')
# df8 = pd.read_csv('Tweets/ChavezVive15-08-14.csv', sep= ';')
# df9 = pd.read_csv('Tweets/ChavezVive15-08-15.csv', sep= ';')
df9 = pd.read_csv('Tweets/ChavezVive15-08-16.csv', sep= ';')
# -----------------------
df10 = pd.read_csv('Tweets/chavezvive_17-01.csv', sep= ';')
df11 = pd.read_csv('Tweets/chavezvive_17-02.csv', sep= ';')
df12 = pd.read_csv('Tweets/chavezvive_17-03.csv', sep= ';')
df13 = pd.read_csv('Tweets/chavezvive_17-04.csv', sep= ';')
df14 = pd.read_csv('Tweets/chavezvive_17-05.csv', sep= ';')
df15 = pd.read_csv('Tweets/chavezvive_17-06.csv', sep= ';')
df16 = pd.read_csv('Tweets/chavezvive_17-07.csv', sep= ';')
df17 = pd.read_csv('Tweets/constituyenteva_17-05.csv', sep= ';')
df18 = pd.read_csv('Tweets/constituyenteva_17-06.csv', sep= ';')
df19 = pd.read_csv('Tweets/constituyenteva_17-07.csv', sep= ';')
# -----------------------
df20 = pd.read_csv('Tweets/selected_users.csv', sep =';')


# Getting the username of the tweets
ids = df1.username 
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
ids14 = df14.username
ids15 = df15.username
ids16 = df16.username
ids17 = df17.username
ids18 = df18.username
ids19 = df19.username
ids20 = df20.username


ids = ids.append(ids2)
ids = ids.append(ids3)
ids = ids.append(ids4)
ids = ids.append(ids5)
ids = ids.append(ids6)
ids = ids.append(ids7)
ids = ids.append(ids8)
ids = ids.append(ids9)
ids = ids.append(ids10)
ids = ids.append(ids11)
ids = ids.append(ids12)
ids = ids.append(ids13)
ids = ids.append(ids14)
ids = ids.append(ids15)
ids = ids.append(ids16)
ids = ids.append(ids17)
ids = ids.append(ids18)
ids = ids.append(ids19)
#ids = ids.append(ids20)

#ids = ids.append(ids11)

ids = pd.Series(ids.unique())
print(ids.size)


CONSUMER_KEY = '6k5VwFN7tsLM6mAQE7NIyWosM'
CONSUMER_SECRET = 'Tnzvldr5fPcm4R6nyup9hESJdPcC9BWlEeaUsZEH14fl6CoynE'
ACCESS_KEY = '86460420-vEpczQ6SSvtOq8ydZwJ61gycLLAgMvxaUylViQUS8'
ACCESS_SECRET = 'vgqVspKrnlIIrw6jvlbPDcV91JKm0poJmpjQsrKWXUKaa'
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

out = open("no_bots_16835-18335.csv", 'w')


mashape_key = "iykKYyk7XTmshsUERrKagp0XxruZp1mWfoEjsnS24G5TOEopR1"
twitter_app_auth = {
    'consumer_key': CONSUMER_KEY,
    'consumer_secret': CONSUMER_SECRET,
    'access_token': ACCESS_KEY,
    'access_token_secret': ACCESS_SECRET,
  }

bom = botometer.Botometer(mashape_key=mashape_key, **twitter_app_auth)

out.write("username\n")

# for user in ids11:
#     out.write(user + "\n")

i = 0
for user in ids[16835:18335]:
    i = i + 1
    try:
        result = bom.check_account(user)
        #print(result['scores']['universal'])
        print(i)

        if result['scores']['universal'] < 0.5:
            out.write(user + "\n")

    except Exception, e:
        print(user)
    
out.close()

# for i in ids:
#     ids_s.append(i.partition(' ')[0])