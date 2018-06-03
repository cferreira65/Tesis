from langdetect import detect, DetectorFactory
import Stemmer

# DetectorFactory.seed = 0

def robust_decode(bs):
    '''Takes a byte string as param and convert it into a unicode one.
First tries UTF8, and fallback to Latin1 if it fails'''
    cr = None
    try:
        cr = bs.decode('utf8')
    except UnicodeDecodeError:
        cr = bs.decode('latin1')
    return cr

def get_language(sentence):
	lang = detect(sentence)

	if lang == 'es':
		return 'spanish'
	elif lang == 'pt':
		return 'portuguese'
	elif lang == 'fr':
		return 'french'
	elif lang == 'it':
		return 'italian'
	else:
		return 'english'

data = []
fp = open('stopwords/opos_stopwords.txt', 'r')
line = fp.readline()
# fp2 = open('stopwords/chav_stopwords.txt', 'r')

# while line:
#     #data.append(line.split(';'))
#     #line = fp.readline()

data = line.split(';')
user = data.pop(0)
result = []

new_text = ""
for twt in data: 
	stemmer = Stemmer.Stemmer(get_language(robust_decode(twt)))
	for word in twt.split():
		new_text = new_text + stemmer.stemWord(word) + " "
	result.append(new_text)

print(result)


    # user.append(data[1:-1])
    # if target_dictionary[data[-1]] == 2:
    #     clas.append(1)
    # else:
    #     clas.append(target_dictionary[data[-1]])
    #line = fp.readline()

# line = fp2.readline()

# while line:
#     #data.append(line.split(';'))
#     #line = fp.readline()

#     data = line.split(';')
#     user.append(data[1:-1])
#     if target_dictionary[data[-1]] == 2:
#         clas.append(0)
#     else:
#         clas.append(target_dictionary[data[-1]])
#     line = fp2.readline()

fp.close
#fp2.close


# new_text = ""
# for word in text.split():
# 	new_text = new_text + stemmer.stemWord(word) + " "


# print(new_text)

