#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import string
import pandas as pd
from nltk.corpus import stopwords


#df1 = pd.read_csv('oposTimelineText.csv', sep= ';')
#print(df1.iloc[0])

data = []
fp = open('../timelines/oposTimelineText.csv', 'r')
line = fp.readline()
out = open("opos_stopwords.txt", 'w')

while line:
    #data.append(line.split(';'))
    #line = fp.readline()

    data = line.split(';')
    # stop words
    train_data = ""
    out.write(data[0])
    out.write(";")
    for d in data[1:-1]:
        d = d.lower()
        filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
        filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
        train_data = ' '.join(word for word in filtered_words)
        out.write(train_data)
        out.write(";")
    
    out.write(data[-1])     
    line = fp.readline()


fp.close
out.close

data = []
fp2 = open('../timelines/chavTimelineText.csv', 'r')
line = fp2.readline()
out2 = open("chav_stopwords.txt", 'w')

while line:
    #data.append(line.split(';'))
    #line = fp.readline()

    data = line.split(';')
    # stop words
    train_data = ""
    out2.write(data[0])
    out2.write(";")
    for d in data[1:-1]:
        d = d.lower()
        filtered_words = list(filter(lambda word: word not in stopwords.words('spanish'), d.split()))
        filtered_words = list(filter(lambda word: word not in stopwords.words('english'), filtered_words))
        train_data = ' '.join(word for word in filtered_words)
        out2.write(train_data)
        out2.write(";")

    out2.write(data[-1])
    line = fp2.readline()


fp2.close
out2.close