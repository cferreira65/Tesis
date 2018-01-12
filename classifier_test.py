#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import string
import pandas as pd
import numpy as np
from array import array
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
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

target_dictionary = {'Chavista\n': 0, 'Oposición\n': 1, 'Ninguno\n':2}

target = array('i')
data = []
fp = open('oposTimelineText.csv', 'r')
line = fp.readline()
fp2 = open('chavTimelineText.csv', 'r')


user1 = []
clas1 = []
user2 = []
clas2 = []
train_data = []


while line:
    #data.append(line.split(';'))
    #line = fp.readline()

    data = line.split(';')
    user1.append(data[1:-1])
    clas1.append(target_dictionary[data[-1]])
    line = fp.readline()

line = fp2.readline()

while line:
    #data.append(line.split(';'))
    #line = fp.readline()

    data = line.split(';')
    user2.append(data[1:-1])
    clas2.append(target_dictionary[data[-1]])
    line = fp2.readline()


fp.close
fp2.close

i = 0

for data in user1[:500]:
    for d in data:
        filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
        filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
        train_data.append(' '.join(word for word in filtered_words))
        target.append(clas1[i])
    
    i = i +1

j = 0
for data in user2[:500]:
    for d in data:
        filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
        filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
        train_data.append(' '.join(word for word in filtered_words))
        target.append(clas2[j])
    
    j = j +1

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

NBprediction = []
SGDprediction = []
test_clasification = []

for data in user1[500:]:
    test_data = []

    for d in data:
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
    test_clasification.append(clas1[i])
    i = i + 1

for data in user2[500:]:
    test_data = []

    for d in data:
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
    test_clasification.append(clas2[j])
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