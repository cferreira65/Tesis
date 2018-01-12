#!/usr/bin/env python

import sys
import string
import pandas as pd

t_opos = []
t_chav = []
opos = open('oposTimelineText.csv', 'r')
chav = open('chavTimelineText.csv', 'r')
opos_dict = {}
chav_dict = {}


line = opos.readline()

while line:
	t_opos = line.split(';')
	opos_dict[t_opos[0]] = t_opos[1:-1]
	line = opos.readline()

line = chav.readline()

while line:
	t_chav = line.split(';')
	chav_dict[t_chav[0]] = t_chav[1:-1]
	line = chav.readline()


print(opos_dict)
