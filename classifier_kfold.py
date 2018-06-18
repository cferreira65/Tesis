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
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
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
fp = open('stemming/opos_stemming.txt', 'r')
line = fp.readline()
fp2 = open('stemming/chav_stemming.txt', 'r')


user = []
clas = []
train_data = []

while line:
    #data.append(line.split(';'))
    #line = fp.readline()

    data = line.split(';')
    user.append(data[1:-1])
    clas.append(target_dictionary[data[-1]])
    line = fp.readline()

line = fp2.readline()

while line:
    #data.append(line.split(';'))
    #line = fp.readline()

    data = line.split(';')
    user.append(data[1:-1])
    clas.append(target_dictionary[data[-1]])
    line = fp2.readline()

fp.close
fp2.close

statistic1 = [[], [], []]
statistic2 = [[], [], []]
statistic3 = [[], [], []]
statistic4 = [[], [], []]
statistic5 = [[], [], []]
statistic6 = [[], [], []]
statistic7 = [[], [], []]
statistic8 = [[], [], []]
statistic9 = [[], [], []]
statistic10 = [[], [], []]
statistic11 = [[], [], []]
statistic12 = [[], [], []]
statistic13 = [[], [], []]
statistic14 = [[], [], []]
statistic15 = [[], [], []]
statistic16 = [[], [], []]

kf = StratifiedKFold(n_splits=10, random_state=42, shuffle = True)

i = 1
for train, test in kf.split(user,clas):
    print train
    print test
    train_data = []
    target = array('i')
    for t in train:
        for d in user[t]:
            train_data.append(d)
            target.append(clas[t])

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

    # Clasificadores regresión logística
    # print X_train_counts1
    # print X_train_tfidf1 

    LG1 = LogisticRegression().fit(X_train_counts1, target)
    LG2 = LogisticRegression().fit(X_train_counts2, target)
    LG3 = LogisticRegression().fit(X_train_tfidf1, target)
    LG4 = LogisticRegression().fit(X_train_tfidf2, target)

    # Clasificadores naive bayes
    NB1 = MultinomialNB().fit(X_train_counts1, target)
    NB2 = MultinomialNB().fit(X_train_counts2, target)
    NB3 = MultinomialNB().fit(X_train_tfidf1, target)
    NB4 = MultinomialNB().fit(X_train_tfidf2, target)

    SGD1 = svm.LinearSVC(C=1.0, random_state = 42).fit(X_train_counts1, target)
    print 1
    SGD2 = svm.LinearSVC(C=1.0, random_state = 42).fit(X_train_counts2, target)
    print 2
    SGD3 = svm.LinearSVC(C=1.0, random_state = 42).fit(X_train_tfidf1, target)
    print 3
    SGD4 = svm.LinearSVC(C=1.0, random_state = 42).fit(X_train_tfidf2, target)
    print 4
    SGD5 = svm.LinearSVC(C=0.5, random_state = 42).fit(X_train_counts1, target)
    print 5
    SGD6 = svm.LinearSVC(C=0.5, random_state = 42).fit(X_train_counts2, target)
    print 6
    SGD7 = svm.LinearSVC(C=0.5, random_state = 42).fit(X_train_tfidf1, target)
    print 7
    SGD8 = svm.LinearSVC(C=0.5, random_state = 42).fit(X_train_tfidf2, target)
    print 8

    LG1prediction = []
    LG2prediction = []
    LG3prediction = []
    LG4prediction = []

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

    for t in test:
        test_data = []
        for d in user[t]:
            test_data.append(d)

    # print(test_data)
        X_new_counts1 = count_vect1.transform(test_data)
        X_new_counts2 = count_vect2.transform(test_data)        

        X_new_tfidf1 = tfidf_transformer1.transform(X_new_counts1)
        X_new_tfidf2 = tfidf_transformer2.transform(X_new_counts2)

        predictedLG1 = LG1.predict(X_new_counts1)
        predictedLG2 = LG2.predict(X_new_counts2)

        predictedLG3 = LG3.predict(X_new_tfidf1)
        predictedLG4 = LG4.predict(X_new_tfidf2)

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

        res = result(predictedLG1)
        LG1prediction.append(res)
        res = result(predictedLG2)
        LG2prediction.append(res)
        res = result(predictedLG3)
        LG3prediction.append(res)
        res = result(predictedLG4)
        LG4prediction.append(res)

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
        test_clasification.append(clas[t])

    string = "resultados/res_kfold" + str(i) + ".txt"
    i = i + 1
    out = open(string, 'w')

    print(len(train))
    print(len(test))

    out.write("Estadisticas de LG1(n_gram = (1, 1), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, LG1prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, LG1prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, LG1prediction, average='weighted')
    statistic1[0].append(res[0])
    statistic1[1].append(res[1])
    statistic1[2].append(res[2])

    out.write("Estadisticas de LG2(n_gram = (1, 2), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, LG2prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, LG2prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, LG2prediction, average='weighted')
    statistic2[0].append(res[0])
    statistic2[1].append(res[1])
    statistic2[2].append(res[2])

    out.write("Estadisticas de LG3(n_gram = (1, 1), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, LG3prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, LG3prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, LG3prediction, average='weighted')
    statistic3[0].append(res[0])
    statistic3[1].append(res[1])
    statistic3[2].append(res[2])

    out.write("Estadisticas de LG4(n_gram = (1, 2), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, LG4prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, LG4prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, LG4prediction, average='weighted')
    statistic4[0].append(res[0])
    statistic4[1].append(res[1])
    statistic4[2].append(res[2])

    out.write("Estadisticas de NB1(n_gram = (1, 1), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, NB1prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, NB1prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, NB1prediction, average='weighted')
    statistic5[0].append(res[0])
    statistic5[1].append(res[1])
    statistic5[2].append(res[2])

    out.write("Estadisticas de NB2(n_gram = (1, 2), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, NB2prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, NB2prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, NB2prediction, average='weighted')
    statistic6[0].append(res[0])
    statistic6[1].append(res[1])
    statistic6[2].append(res[2])

    out.write("Estadisticas de NB3(n_gram = (1, 1), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, NB3prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, NB3prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, NB3prediction, average='weighted')
    statistic7[0].append(res[0])
    statistic7[1].append(res[1])
    statistic7[2].append(res[2])

    out.write("Estadisticas de NB4(n_gram = (1, 2), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, NB4prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, NB4prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, NB4prediction, average='weighted')
    statistic8[0].append(res[0])
    statistic8[1].append(res[1])
    statistic8[2].append(res[2])

    out.write("Estadisticas de SVM1(C = 1.0, n_gram = (1, 1), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD1prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD1prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD1prediction, average='weighted')
    statistic9[0].append(res[0])
    statistic9[1].append(res[1])
    statistic9[2].append(res[2])

    out.write("Estadisticas de SVM2(C = 1.0, n_gram = (1, 2), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD2prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD2prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD2prediction, average='weighted')
    statistic10[0].append(res[0])
    statistic10[1].append(res[1])
    statistic10[2].append(res[2])

    out.write("Estadisticas de SVM3(C = 1.0, n_gram = (1, 1), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD3prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD3prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD3prediction, average='weighted')
    statistic11[0].append(res[0])
    statistic11[1].append(res[1])
    statistic11[2].append(res[2])

    out.write("Estadisticas de SVM4(C = 1.0, n_gram = (1, 2), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD4prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD4prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD4prediction, average='weighted')
    statistic12[0].append(res[0])
    statistic12[1].append(res[1])
    statistic12[2].append(res[2])

    out.write("Estadisticas de SVM5(C = 0.5, n_gram = (1, 1), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD5prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD5prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD5prediction, average='weighted')
    statistic13[0].append(res[0])
    statistic13[1].append(res[1])
    statistic13[2].append(res[2])

    out.write("Estadisticas de SVM6(C = 0.5, n_gram = (1, 2), tf-idf = False):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD6prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD6prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD6prediction, average='weighted')
    statistic14[0].append(res[0])
    statistic14[1].append(res[1])
    statistic14[2].append(res[2])

    out.write("Estadisticas de SVM7(C = 0.5, n_gram = (1, 1), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD7prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD7prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD7prediction, average='weighted')
    statistic15[0].append(res[0])
    statistic15[1].append(res[1])
    statistic15[2].append(res[2])

    out.write("Estadisticas de SVM8(C = 0.5, n_gram = (1, 2), tf-idf = True):\n")

    out.write(str(metrics.classification_report(test_clasification, SGD8prediction,
            target_names=["Chavista","Opositor","Ninguno"])))

    out.write(str(metrics.confusion_matrix(test_clasification, SGD8prediction)))

    out.write("\n")

    res = metrics.precision_recall_fscore_support(test_clasification, SGD8prediction, average='weighted')
    statistic16[0].append(res[0])
    statistic16[1].append(res[1])
    statistic16[2].append(res[2])

    out.close()


out = open("resultados/avg_kfold.txt", 'w')

out.write("Promedio de LG1:\n")
out.write("Precision: " + str(np.mean(statistic1[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic1[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic1[2])) + "\n")

out.write("\nPromedio de LG2:\n")
out.write("Precision: " + str(np.mean(statistic2[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic2[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic2[2])) + "\n")

out.write("\nPromedio de LG3:\n")
out.write("Precision: " + str(np.mean(statistic3[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic3[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic3[2])) + "\n")

out.write("\nPromedio de LG4:\n")
out.write("Precision: " + str(np.mean(statistic4[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic4[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic4[2])) + "\n")

out.write("\nPromedio de NB1:\n")
out.write("Precision: " + str(np.mean(statistic5[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic5[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic5[2])) + "\n")

out.write("\nPromedio de NB2:\n")
out.write("Precision: " + str(np.mean(statistic6[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic6[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic6[2])) + "\n")

out.write("\nPromedio de NB3:\n")
out.write("Precision: " + str(np.mean(statistic7[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic7[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic7[2])) + "\n")

out.write("\nPromedio de NB4:\n")
out.write("Precision: " + str(np.mean(statistic8[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic8[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic8[2])) + "\n")

out.write("\nPromedio de SVM1:\n")
out.write("Precision: " + str(np.mean(statistic9[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic9[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic9[2])) + "\n")

out.write("\nPromedio de SVM2:\n")
out.write("Precision: " + str(np.mean(statistic10[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic10[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic10[2])) + "\n")

out.write("\nPromedio de SVM3:\n")
out.write("Precision: " + str(np.mean(statistic11[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic11[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic11[2])) + "\n")

out.write("\nPromedio de SVM4:\n")
out.write("Precision: " + str(np.mean(statistic12[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic12[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic12[2])) + "\n")

out.write("\nPromedio de SVM5:\n")
out.write("Precision: " + str(np.mean(statistic13[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic13[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic13[2])) + "\n")

out.write("\nPromedio de SVM6:\n")
out.write("Precision: " + str(np.mean(statistic14[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic14[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic14[2])) + "\n")

out.write("\nPromedio de SVM7:\n")
out.write("Precision: " + str(np.mean(statistic15[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic15[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic15[2])) + "\n")

out.write("\nPromedio de SVM8:\n")
out.write("Precision: " + str(np.mean(statistic16[0])) + "\n")
out.write("Recall: " + str(np.mean(statistic16[1])) + "\n")
out.write("Fscore: " + str(np.mean(statistic16[2])) + "\n")

out.close()
