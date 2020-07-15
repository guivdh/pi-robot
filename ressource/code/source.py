from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import speech_recognition as sr
import bluetooth
from gtts import gTTS
import sys
from mutagen.mp3 import MP3
from time import sleep
from playsound import playsound
import nltk
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
from nltk.stem.lancaster import LancasterStemmer
import threading
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

mois={1:'janvier',2:'février',3:'mars',4:'avril',5:'mai',6:'juin',7:'juillet',8:'août',9:'septembre',10:'octobre',11:'novembre',12:'décembre'}
moisNbre={'janvier':1,'février':2,'mars':3,'avril':4,'mai':5,'juin':6,'juillet':7,'août':8,'septembre':9,'octobre':10,'novembre':11,'décembre':12}

serverMACAddress = '98:D3:33:F5:AE:4D'
port = 1

# ---------------------------------------------------- IA Initialisation
nltk.download('punkt')
stemmer = LancasterStemmer()

with open("IA-conversation/json file/intents.json", encoding='utf-8') as file:
    data = json.load(file)

try:
    with open("IA-conversation/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("IA-conversation/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("IA-conversation/model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("IA-conversation/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


#Connection au bluetooth
#try:
#    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#    s.connect((serverMACAddress, port))
#except Exception as e:
#    print("Exception : " + str(e))
#    print("Une erreur est survenue")
#    audio = MP3("sounds/erreur.mp3")
#    player = os.system("mpg123 "+"sounds/erreur.mp3")
#    speakEnglish(str(e))
#    sys.exit()

def get_audio():
    r = sr.Recognizer()
    print('En écoute !')
    player = os.system("mpg123 "+'sounds/pop.mp3')
    mic = sr.Microphone()
    with mic as source:
        audioSon = r.listen(source)
        #player = os.system("mpg123 "+'sounds/pop.mp3')
        said = ""

        try:
            said = r.recognize_google(audioSon, language='fr-FR')
            print(said)
        except Exception as e:
            print("Exception : " + str(e))
            os.system("mpg123 "+"sounds/erreur.mp3")
    return said

def minuteur(nb):
    for i in range(nb):
        time.sleep(1)
    os.system("mpg123 sounds/alarme.mp3")



# Lancement du programme
player = os.system("mpg123 "+'sounds/actionChoix.mp3')
while 1:

    text = ""
    # commande = get_audio()

    global responses
    global commande
    print("Start talking with the bot (type quit to stop)!")
    inp = input("You: ")
    if inp.lower() == "quit":
        break

    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    print(tag)
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
    print(responses)
    length = len(responses)
    nbr = random.randint(0, length - 1)
    commande = tag
    tag = tag.replace(" ", "-")
    phrase = tag + "-" + str(nbr)
    os.system("mpg123" + " sounds/" + phrase + ".mp3")
    print(responses[nbr])

    print(commande)

    if commande == "blague":
        os.system("python3 API-requests/getJoke.py")

    if commande == "lire évènements à venir":
        player = os.system("mpg123 "+'sounds/rechercheCalendrier.mp3')
        os.system("python3 calendar/getEvents.py")

    if commande == "actualité":
        os.system("python3 API-requests/getNews.py")

    if commande == "mettre un minuteur":
        txt = inp.split("de")
        if "secon" in txt[1]:
            nbr = int(re.search(r'\d+', txt[1]).group())
            strg = "Très bien, je lance un minuteur de " + str(nbr) + " secondes"
            os.system("python3 talking/tts.py '" + strg + "'")
            a = threading.Thread(None, minuteur, None, (nbr,))
            a.start()
        if "minute" in txt[1]:
            nbr = int(re.search(r'\d+', txt[1]).group())
            strg = "Très bien, je lance un minuteur de " + str(nbr) + " minutes"
            os.system("python3 talking/tts.py '" + strg + "'")
            a = threading.Thread(None, minuteur, None, (nbr*60,))
            a.start()
        if "heure" in txt[1]:
            nbr = int(re.search(r'\d+', txt[1]).group())
            strg = "Très bien, je lance un minuteur de " + str(nbr) + " heures"
            os.system("python3 talking/tts.py '" + strg + "'")
            a = threading.Thread(None, minuteur, None, (nbr * 3600,))
            a.start()
            
    if("donne-moi les événements du" in commande):
        rep = commande.split()
        longueur = len(rep)
        print('Mois = ' + str(moisNbre[rep[longueur-1]]))
        print('Jour = ' + rep[longueur-2])
        os.system("python3 calendar/getEventsDay.py '"+str(rep[longueur-2])+'\' \''+str(moisNbre[rep[longueur-1]])+'\'')
        #speak("Je recherche les événements du " + )
        #os.system("python3 calendar/getEventsDay.py")

    if commande == "allume la LED":
        text = 'on'
        os.system("mpg123 "+'sounds/ledON.mp3')

    if commande == "éteins la LED":
        text = 'off'
        os.system("mpg123 "+'sounds/ledOFF.mp3')

    if commande == "donne-moi la température":
        s.send("temperature")
        data1 = s.recv(1024)
        time.sleep(0.5)
        s.send("temperature")
        data2 = s.recv(1024)
        data = data1+data2
        strg = "Il fait actuellement" + data.decode("utf-8") + "degré dans la pièce"
        speak(strg)

    if commande == "balade toi":
        s.send("deplacement")

    if commande == "arrête de te balader":
        s.send("arret")

    if commande == "tu peux quitter":
        # Local time without timezone information printed in ISO 8601 format
        date1 = datetime.datetime(1996, 12, 11)

        # Date time separator is a "#" symbol
        min=(date1.isoformat("T"))
        print(min)
        break


    #s.send(text)
