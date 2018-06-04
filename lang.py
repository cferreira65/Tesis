from langdetect import detect, DetectorFactory
import Stemmer

# DetectorFactory.seed = 0

def quit_character(character, text):
    new_text = ""
    for i in text.replace('\n','').encode('utf-8'):
        new_text =  new_text + i.strip(character)

    return new_text 

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
out1 = open("timelines/oposTimelineStemming.csv", 'w')
line = fp.readline()
fp2 = open('stopwords/chav_stopwords.txt', 'r')
out2 = open("timelines/chavTimelineStemming.csv", 'w')
opos = []
chav = []

while line:

	data = line.split(';')
	user = [data.pop(0)]
	result = []

	new_text = ""
	for twt in data:
		try: 
			twt = robust_decode(twt)
			stemmer = Stemmer.Stemmer(get_language(twt))
			for word in twt.split():
				new_text = new_text + stemmer.stemWord(word) + " "
			print(new_text)
			result.append(new_text)
		except:
			result.append(twt)

	opos.append(user.append(result))
	line = fp.readline()

i = 0
for user in opos:
    try:
        for tw in user:
            out1.write(quit_character(';', tw.text))
            out1.write(";")
		
		
    except Exception, e:
        print(user)
        i = i + 1
        print(e)

	out1.write("\n")
        i = i + 1
	

fp.close
out1.close()

line = fp2.readline()

while line:

	data = line.split(';')
	user = [data.pop(0)]
	result = []

	new_text = ""
	for twt in data:
		try: 
			twt = robust_decode(twt)
			stemmer = Stemmer.Stemmer(get_language(twt))
			for word in twt.split():
				new_text = new_text + stemmer.stemWord(word) + " "
			print(new_text)
			result.append(new_text)
		except:
			result.append(twt)

	chav.append(user.append(result))
	line = fp2.readline()


i = 0
for user in chav:
    try:
        for tw in timeline:
            out2.write(quit_character(';', tw.text))
            out2.write(";")

    except Exception, e:
        print(user)
        i = i + 1
        print(e)

	out2.write("\n")
    i = i + 1
	
out2.close()
fp2.close
