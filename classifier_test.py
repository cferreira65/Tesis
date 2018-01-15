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
        train_data.append(d)
        target.append(clas1[i])
    
    i = i +1

j = 0
for data in user2[:500]:
    for d in data:
        train_data.append(d)
        target.append(clas2[j])
    
    j = j +1

count_vect1 = CountVectorizer()
count_vect2 = CountVectorizer(ngram_range = (1,2))

X_train_counts1 = count_vect1.fit_transform(train_data)
X_train_counts2 = count_vect2.fit_transform(train_data)

#print(X_train_counts.shape)
#print(count_vect.vocabulary_.get(u'búsqueda'))

tfidf_transformer1 = TfidfTransformer()
tfidf_transformer2 = TfidfTransformer()

X_train_tfidf1 = tfidf_transformer1.fit_transform(X_train_counts1)
X_train_tfidf2 = tfidf_transformer2.fit_transform(X_train_counts2)

# Clasificadores naive bayes
NB1 = MultinomialNB().fit(X_train_counts1, target)
NB2 = MultinomialNB().fit(X_train_counts2, target)
NB3 = MultinomialNB().fit(X_train_tfidf1, target)
NB4 = MultinomialNB().fit(X_train_tfidf2, target)


SGD1 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=5, tol=None).fit(X_train_counts1, target)
SGD2 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=5, tol=None).fit(X_train_counts2, target)
SGD3 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=5, tol=None).fit(X_train_tfidf1, target)
SGD4 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=5, tol=None).fit(X_train_tfidf2, target)
SGD5 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-2, random_state=42,
                    max_iter=5, tol=None).fit(X_train_counts1, target)
SGD6 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-2, random_state=42,
                    max_iter=5, tol=None).fit(X_train_counts2, target)
SGD7 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-2, random_state=42,
                    max_iter=5, tol=None).fit(X_train_tfidf1, target)
SGD8 = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-2, random_state=42,
                    max_iter=5, tol=None).fit(X_train_tfidf2, target)


NB1prediction = []
NB2prediction = []
NB3prediction = []
NB4prediction = []

SGD1prediction = []
SGD2prediction = []
SGD3prediction = []
SGD4prediction = []
SGD5prediction = []
SGD6prediction = []
SGD7prediction = []
SGD8prediction = []

test_clasification = []

for data in user1[500:]:
    test_data = []

    for d in data:
        test_data.append(d)

    # print(test_data)
    X_new_counts1 = count_vect1.transform(test_data)
    X_new_counts2 = count_vect2.transform(test_data)        

    X_new_tfidf1 = tfidf_transformer1.transform(X_new_counts1)
    X_new_tfidf2 = tfidf_transformer2.transform(X_new_counts2)

    predictedNB1 = NB1.predict(X_new_counts1)
    predictedNB2 = NB2.predict(X_new_counts2)

    predictedNB3 = NB3.predict(X_new_tfidf1)
    predictedNB4 = NB4.predict(X_new_tfidf2)

    # predicted = text_clf.predict(test_data)
    predictedSGD1 = SGD1.predict(X_new_counts1)
    predictedSGD2 = SGD2.predict(X_new_counts2)
    predictedSGD3 = SGD3.predict(X_new_tfidf1)
    predictedSGD4 = SGD4.predict(X_new_tfidf2)
    predictedSGD5 = SGD5.predict(X_new_counts1)
    predictedSGD6 = SGD6.predict(X_new_counts2)
    predictedSGD7 = SGD7.predict(X_new_tfidf1)
    predictedSGD8 = SGD8.predict(X_new_tfidf2)


    res = result(predictedNB1)
    NB1prediction.append(res)
    res = result(predictedNB2)
    NB2prediction.append(res)
    res = result(predictedNB3)
    NB3prediction.append(res)
    res = result(predictedNB4)
    NB4prediction.append(res)
    #print("La predicción de NB es: " + str(res))
    
    res = result(predictedSGD1)
    SGD1prediction.append(res)
    res = result(predictedSGD2)
    SGD2prediction.append(res)  
    res = result(predictedSGD3)
    SGD3prediction.append(res)  
    res = result(predictedSGD4)
    SGD4prediction.append(res)  
    res = result(predictedSGD5)
    SGD5prediction.append(res)  
    res = result(predictedSGD6)
    SGD6prediction.append(res)  
    res = result(predictedSGD7)
    SGD7prediction.append(res)  
    res = result(predictedSGD8)
    SGD8prediction.append(res)          
    #print("La predicción de SGD es: " + str(res))
    test_clasification.append(clas1[i])
    i = i + 1

for data in user2[500:]:
    test_data = []

    for d in data:
        test_data.append(d)

    # print(test_data)
    X_new_counts1 = count_vect1.transform(test_data)
    X_new_counts2 = count_vect2.transform(test_data)        

    X_new_tfidf1 = tfidf_transformer1.transform(X_new_counts1)
    X_new_tfidf2 = tfidf_transformer2.transform(X_new_counts2)

    predictedNB1 = NB1.predict(X_new_counts1)
    predictedNB2 = NB2.predict(X_new_counts2)

    predictedNB3 = NB3.predict(X_new_tfidf1)
    predictedNB4 = NB4.predict(X_new_tfidf2)

    # predicted = text_clf.predict(test_data)
    predictedSGD1 = SGD1.predict(X_new_counts1)
    predictedSGD2 = SGD2.predict(X_new_counts2)
    predictedSGD3 = SGD3.predict(X_new_tfidf1)
    predictedSGD4 = SGD4.predict(X_new_tfidf2)
    predictedSGD5 = SGD5.predict(X_new_counts1)
    predictedSGD6 = SGD6.predict(X_new_counts2)
    predictedSGD7 = SGD7.predict(X_new_tfidf1)
    predictedSGD8 = SGD8.predict(X_new_tfidf2)


    res = result(predictedNB1)
    NB1prediction.append(res)
    res = result(predictedNB2)
    NB2prediction.append(res)
    res = result(predictedNB3)
    NB3prediction.append(res)
    res = result(predictedNB4)
    NB4prediction.append(res)
    #print("La predicción de NB es: " + str(res))
    
    res = result(predictedSGD1)
    SGD1prediction.append(res)
    res = result(predictedSGD2)
    SGD2prediction.append(res)  
    res = result(predictedSGD3)
    SGD3prediction.append(res)  
    res = result(predictedSGD4)
    SGD4prediction.append(res)  
    res = result(predictedSGD5)
    SGD5prediction.append(res)  
    res = result(predictedSGD6)
    SGD6prediction.append(res)  
    res = result(predictedSGD7)
    SGD7prediction.append(res)  
    res = result(predictedSGD8)
    SGD8prediction.append(res)          
    #print("La predicción de SGD es: " + str(res))
    test_clasification.append(clas2[j])
    j = j + 1 


#fp1 = open('resultNB.txt', 'a')
#fp2 = open('resultSVM.txt', 'a')

# print(train_data)
print(predictedNB1)
print(predictedSGD1)

# print(predicted)

print(len(train_data))
print(len(target))

print("Estadisticas de NB1:")

print(metrics.classification_report(test_clasification, NB1prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, NB1prediction))

print("Estadisticas de NB2:")

print(metrics.classification_report(test_clasification, NB2prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, NB2prediction))

print("Estadisticas de NB3:")

print(metrics.classification_report(test_clasification, NB3prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, NB3prediction))

print("Estadisticas de NB4:")

print(metrics.classification_report(test_clasification, NB4prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, NB4prediction))

print("Estadisticas de SVM1:")

print(metrics.classification_report(test_clasification, SGD1prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD1prediction))

print("Estadisticas de SVM2:")

print(metrics.classification_report(test_clasification, SGD2prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD2prediction))

print("Estadisticas de SVM3:")

print(metrics.classification_report(test_clasification, SGD3prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD3prediction))

print("Estadisticas de SVM4:")

print(metrics.classification_report(test_clasification, SGD4prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD4prediction))

print("Estadisticas de SVM5:")

print(metrics.classification_report(test_clasification, SGD5prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD5prediction))

print("Estadisticas de SVM6:")

print(metrics.classification_report(test_clasification, SGD6prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD6prediction))

print("Estadisticas de SVM7:")

print(metrics.classification_report(test_clasification, SGD7prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD7prediction))

print("Estadisticas de SVM8:")

print(metrics.classification_report(test_clasification, SGD8prediction,
        target_names=["Chavista","Opositor","Ninguno"]))

print(metrics.confusion_matrix(test_clasification, SGD8prediction))
