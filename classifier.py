#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import pandas as pd
import tweepy
import simplejson
import numpy as np
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from array import array
from nltk.corpus import stopwords

def result(lis):
    count = [0,0,0]

    for prediction in lis:
        count[prediction] = count[prediction] + 1

    if (count[0] == count[1]):
        res = 2
    elif (count[0] > count[1] and count[0] > count[2]):
        res = 0
    elif (count[1] > count[0] and count[1] > count[2]):
        res = 1
    else:
        res = 2
    return res

df1 = pd.read_csv('users_opos_test.csv', sep= ',')
df2 = pd.read_csv('users_chav_test.csv', sep= ',')

target = array('i')
data = []

user = df1.User
user2 = df2.User

print (df1.Carlos)
target_dictionary = {'Chavista': 0, 'Oposición': 1, 'Ninguno':2}

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
 # Opositores
i = 0
for u in user[:500]:
    try:
        user_object = api.get_user(screen_name = u) 
        description = user_object.description
        timeline = api.user_timeline(screen_name = u)
        classification = target_dictionary[df1.Carlos[i]]
        data.append(description)
        target.append(classification)
        print(i)
        i = i + 1
        for tweet in timeline:
            data.append(tweet.text)
            target.append(classification)
    except Exception, e:
        print(u)
        i = i + 1

# chavistas
j = 0
for u in user2[:500]:
    try:
        user_object = api.get_user(screen_name = u) 
        description = user_object.description
        timeline = api.user_timeline(screen_name = u)
        classification = target_dictionary[df2.Carlos[j]]
        data.append(description)
        target.append(classification)
        print(j)
        j = j + 1

        for tweet in timeline:
            data.append(tweet.text)
            target.append(classification)
    except Exception, e:
        print(u)
        j = j + 1



# text_clf = Pipeline([('vect', CountVectorizer()),
#                     ('tfidf', TfidfTransformer()),
#                     ('clf', MultinomialNB()),
# ])

# text_clf.fit(train_data, target)

# stop words
train_data = []
for d in data:
    # print(i.split())
    filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
    filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
    train_data.append(' '.join(word for word in filtered_words))

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train_data)
print(X_train_counts.shape)
print(count_vect.vocabulary_.get(u'búsqueda'))

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, target)
clf2 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=5, tol=None).fit(X_train_tfidf, target)

# print(X_train_counts.shape)
# print(count_vect.vocabulary_.get(u'sigue'))
# print(X_train_tfidf.shape)

NBprediction = []
SGDprediction = []
test_clasification = []
for u in user[500:1050]:
    try:
        data2 = []
        test_data = []
        user_object = api.get_user(screen_name = u) 
        description = user_object.description
        timeline = api.user_timeline(screen_name = u)
        classification = target_dictionary[df1.Carlos[i]]
        print(i)
        i = i + 1

        data2.append(description)        
        # target.append(classification)
        for tweet in timeline:
            data2.append(tweet.text)
            # target.append(classification)            
        for d in data2:
            # print(i.split())
            filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
            filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
            test_data.append(' '.join(word for word in filtered_words))


        # print(test_data)
        X_new_counts = count_vect.transform(test_data)        
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        predictedNB = clf.predict(X_new_tfidf)
        # predicted = text_clf.predict(test_data)
        predictedSGD = clf2.predict(X_new_tfidf)
        res = result(predictedNB)
        NBprediction.append(res)
        print("La predicción de NB es: " + str(res))
        res = result(predictedSGD)
        SGDprediction.append(res)        
        print("La predicción de SGD es: " + str(res))
        test_clasification.append(classification)



    except Exception, e:
        print(u)
        i = i + 1



for u in user2[500:1050]:
    try:
        data2 = []
        test_data = []
        user_object = api.get_user(screen_name = u) 
        description = user_object.description
        timeline = api.user_timeline(screen_name = u)
        data2.append(description)        
        classification = target_dictionary[df2.Carlos[j]]
        print(j)
        j = j + 1

        # target.append(classification)
        for tweet in timeline:
            data2.append(tweet.text)
            # target.append(classification)            
        for d in data2:
            # print(i.split())
            filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
            filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
            test_data.append(' '.join(word for word in filtered_words))


        # print(test_data)
        X_new_counts = count_vect.transform(test_data)        
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)
        predictedNB = clf.predict(X_new_tfidf)
        # predicted = text_clf.predict(test_data)
        predictedSGD = clf2.predict(X_new_tfidf)
        res = result(predictedNB)
        NBprediction.append(res)
        print("La predicción de NB es: " + str(res))
        res = result(predictedSGD)
        SGDprediction.append(res)        
        print("La predicción de SGD es: " + str(res))
        test_clasification.append(classification)



    except Exception, e:
        print(u)
        j = j + 1


# print(train_data)
print(predictedNB)
print(predictedSGD)

# print(predicted)

print(len(train_data))
print(len(target))

print("Estadisticas de NB:")

print(metrics.classification_report(test_clasification, NBprediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, NBprediction))

print("Estadisticas de SVM:")

print(metrics.classification_report(test_clasification, SGDprediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGDprediction))