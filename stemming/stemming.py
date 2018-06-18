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
fp = open('../stopwords/opos_stopwords.txt', 'r')
out1 = open("opos_stemming.txt", 'w')

fp2 = open('../stopwords/chav_stopwords.txt', 'r')
out2 = open("chav_stemming.txt", 'w')
opos = []
chav = []

# leo la primera linea
line = fp.readline()

while line:

	#  divido la linea leia en cada item del csv
	data = line.split(';')
	#  elimino el usuario de la lista (no debe hacerse stemming de el)
	user = [data[0]]

	#  para cada tweet o bio de la linea leida
	for twt in data[1:-1]:
		new_text = "" # nuevo texto stemmed
		try: 
			twt = robust_decode(twt) # decode de caracteres y emojis
			stemmer = Stemmer.Stemmer(get_language(twt)) # deteccion de idioma e inicializacion del stemming

			for word in twt.split(): # para cada palabra del tweet 
				# aplico stemming en la palabra y reconstruyo el string
				new_text = new_text + stemmer.stemWord(word) + " " 

			# agrego el tweet ya stemmed a los datos del ususario
			user.append(new_text[:-1])

		# si falla, agrego el tweet sin stemming
		except Exception, e:
			user.append(twt)

	# agrego el usuario a la lista de users
	user.append(data[-1])
	opos.append(user)

	# leo una nueva linea
	line = fp.readline()

# cierro el archivo de entrada
fp.close

# para cada usuario en la lista de users
for user in opos:
    try:
    	# para cada tweet del usuario 
        for tw in user[:-1]:
        	# escribo separando con ; (formato csv)
            out1.write(u''.join(tw).encode('utf-8'))
            out1.write(";")
        out1.write(user[-1])
			
	# si hay error muestro el usuario que falla y el error
    except Exception, e:
        print(user)
        print(e)

    # escribo el salto de linea

	
# cierro el archivo de salida
out1.close()

# line = fp2.readline()

# leo la primera linea
line = fp2.readline()
data = []

while line:

	#  divido la linea leia en cada item del csv
	data = line.split(';')
	#  elimino el usuario de la lista (no debe hacerse stemming de el)
	user = [data[0]]

	#  para cada tweet o bio de la linea leida
	for twt in data[1:-1]:
		new_text = "" # nuevo texto stemmed
		try: 
			twt = robust_decode(twt) # decode de caracteres y emojis
			stemmer = Stemmer.Stemmer(get_language(twt)) # deteccion de idioma e inicializacion del stemming

			for word in twt.split(): # para cada palabra del tweet 
				# aplico stemming en la palabra y reconstruyo el string
				new_text = new_text + stemmer.stemWord(word) + " " 

			# agrego el tweet ya stemmed a los datos del ususario
			user.append(new_text[:-1])

		# si falla, agrego el tweet sin stemming
		except Exception, e:
			user.append(twt)

	# agrego el usuario a la lista de users
	user.append(data[-1])
	chav.append(user)

	# leo una nueva linea
	line = fp2.readline()

# cierro el archivo de entrada
fp2.close

# para cada usuario en la lista de users
for user in chav:
    try:
    	# para cada tweet del usuario 
        for tw in user[:-1]:
        	# escribo separando con ; (formato csv)
            out2.write(u''.join(tw).encode('utf-8'))
            out2.write(";")

        out2.write(user[-1])
			
	# si hay error muestro el usuario que falla y el error
    except Exception, e:
        print(user)
        print(e)

    # escribo el salto de linea

	
# cierro el archivo de salida
out2.close()