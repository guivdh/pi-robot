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
import configparser
import pymysql

# Lecture du fichier de configuration
cfg = configparser.ConfigParser()
cfg.read('config/config.cfg')


# Connexion à la base de donnée
mydb = pymysql.connect(
    host="51.77.201.156",
    user="guivdh",
    password="BKD6Vccy9SPRx56k",
    db='master'
)

# cible vers l'api de calendrier google
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

mois = {1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin', 7: 'juillet', 8: 'août', 9: 'septembre',
        10: 'octobre', 11: 'novembre', 12: 'décembre'}
moisNbre = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
            'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12}

# MACAddress du HC-05 sur l'arduino
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

# --------------------------------------------- fin de la configuration de l'IA

# Connection au bluetooth
try:
   s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
   s.connect((serverMACAddress, port))
except Exception as e:
   print("Exception : " + str(e))
   sys.exit()

# Fonction qui permet transforme la voix en texte (api de Google)
def get_audio():
    r = sr.Recognizer()
    print('En écoute !')
    mic = sr.Microphone()
    with mic as source:
        # r.adjust_for_ambient_noise(source)
        audioSon = r.listen(source)
        # player = os.system("mpg123 "+'sounds/pop.mp3')
        said = ""

        # Lance la reconnaissance de voix
        try:
            said = r.recognize_google(audioSon, language='fr-FR')
            print(said)
        except Exception as e:
            print("Exception : " + str(e))
            # os.system("mpg123 "+"sounds/erreur.mp3")
    return said

# Fonction qui transforme un texte en voix de robot
def speak(phrase):
    os.system("python3 talking/tts.py '" + phrase + "'")

# Fonction qui lanceun chronomètre de x secondes
def minuteur(nb):
    for i in range(nb):
        time.sleep(1)
    os.system("mpg123 sounds/alarme.mp3")

"""
    Fonction avec boucle infinie qui émet une alarme lorsque l'heure actuelle correspond à l'heure rentrée en paramètre.
    Les heures sont en format Timestamp
"""
def alarme(alarme):
    while True:
        heure = time.localtime()
        print("Heure : " + str(heure[3]) + 'h' + str(heure[4]) + " - Alarme : " + alarme)
        if alarme == str(heure[3]) + 'h' + str(heure[4]):
            os.system("mpg123 sounds/alarme.mp3")
            break
        time.sleep(1)

# fonction qui gère l'humeur du robot. Toutes les 15 secondes, l'humeur est diminiuée de 1
def humeurMoins():
    while True:
        nbr = cfg.get('bot', 'humeur')
        newNbr = int(nbr) - 1
        cfg.set('bot', 'humeur', str(newNbr))
        cfg.write(open('config/config.cfg', 'w'))
        time.sleep(15)

# fonction qui gère l'humeur du robot. Lorsqu'elle est appelée, elle ajoute 20 à l'humeur
def humeurPlus():
    nbr = cfg.get('bot', 'humeur')
    newNbr = int(nbr) + 20
    cfg.set('bot', 'humeur', str(newNbr))
    cfg.write(open('config/config.cfg', 'w'))


# ------------------------------------------------- Lancement du programme

# Mot pour réveilleur le robot
WAKE = "simbot"

player = os.system("mpg123 " + 'sounds/actionChoix.mp3')

# Lancement du thread qui gère l'humeur
humeur = threading.Thread(None, humeurMoins, None)
humeur.start()

while 1:

    sql = ""
    requestType = ""
    cursor = mydb.cursor()

    # text = get_audio()
    text = input("you: ")
    if text == "quit":
        sys.exit(0)

    # Si simbot est prononcé, le robot se réveil
    # s.send('reveil')
    if text.count(WAKE) > 0:
        os.system("mpg123 " + 'sounds/pop.mp3')

        nom = cfg.get('user', 'nom')

        # Si le nom de l'utilisateur n'a pas encore été enregistrer, Simbot le lui demande
        if nom == "undefined":
            os.system("mpg123 sounds/demandeNom.mp3")
            nom = input("you: ")
            cfg.set('user', 'nom', nom)
            cfg.write(open('config/config.cfg', 'w'))

        # inp = get_audio()
        inp = input("you :")

        global responses
        global commande
        # inp = input("You: ")
        if inp.lower() == "tu peux quitter":
            sys.exit(0)

        # Utilisation de l'IA en y rentrant la commande

        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        print(tag)
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        print(responses)
        length = len(responses)

        # choisit une réponse en fonction de l'humeur du robot
        if length > 0:
            nbr = cfg.get('bot', 'humeur')
            print("Humeur: " + nbr)
            if int(nbr) < 500:
                phraseADire = 0
            elif 1500 > int(nbr) > 500:
                phraseADire = 1
            else:
                phraseADire = random.randint(2, length - 1)
            commande = tag

            # Envoie la commande au robot
            s.send(commande)

            # Faire dire la réponse au robot
            tag = tag.replace(" ", "-")
            phrase = tag + "-" + str(phraseADire)
            #os.system("mpg123" + " sounds/" + phrase + ".mp3")
            print(responses[phraseADire])
            print(commande)

        else:
            commande = tag
            print(responses[0])
            print(commande)

        requestType = 'conversation'

        if commande == "blague":
            os.system("python3 API-requests/getJoke.py")
            requestType = "blague"

        if commande == "lire évènements à venir":
            player = os.system("mpg123 " + 'sounds/rechercheCalendrier.mp3')
            os.system("python3 calendar/getEvents.py")
            requestType = "calendrier"

        if commande == "actualité":
            os.system("python3 API-requests/getNews.py")
            requestType = "actualité"

        if commande == "mettre un minuteur":
            txt = inp.split("de")

            """ 
                Analyse de la commande pour mettre un minuteur. La phrase est séparée par le mot " de "
                Ensuite, en fonction de ce qui est mis dans la phrase, si c'est secondes, minutes ou heures, le nombre
                présent devant sera utilisé pour lancer la fonction adéquate
            """

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
                a = threading.Thread(None, minuteur, None, (nbr * 60,))
                a.start()
            if "heure" in txt[1]:
                nbr = int(re.search(r'\d+', txt[1]).group())
                strg = "Très bien, je lance un minuteur de " + str(nbr) + " heures"
                os.system("python3 talking/tts.py '" + strg + "'")
                a = threading.Thread(None, minuteur, None, (nbr * 3600,))
                a.start()
            requestType = "minuteur"

        if commande == "météo":
            os.system("python3 API-requests/getWeather.py")
            requestType = "météo"

        if commande == "mettre une alarme":

            """
                Sépare la phrase avec le mot 'à'. La partie à droite de à sera analysée pour en resortir l'heure
                en timestamp. Ensuite la fonction threadAlarm sera appelé et prenant comme paramètre le timestamp
            """

            txt = inp.split("à")
            heure = time.localtime()
            print(txt[1].strip())
            threadAlarm = threading.Thread(None, alarme, None, (txt[1].strip(),))
            threadAlarm.start()
            requestType = "alarme"

        if commande == "arrêter l'alarme":
            if threadAlarm.is_alive():
                threadAlarm.terminate()
            else:
                os.system("mpg123" + " sounds/nonAlarme.mp3")

        if commande == "envoyer un mail":
            os.system("mpg123" + " sounds/mail.mp3")
            os.system("mpg123 " + 'sounds/pop.mp3')

            # Demande le destinataire du mail
            dest = get_audio().lower()
            os.system("mpg123" + " sounds/mailCorps.mp3")
            os.system("mpg123 " + 'sounds/pop.mp3')

            # Demande le contenu du mail
            body = get_audio()
            os.system("python3 mail/sendMail.py '" + dest + "' '" + body + "'")
            os.system("mpg123 " + 'sounds/mailEnvoie.mp3')
            requestType = "mail"

        if commande == "ajouter un évènement":

            # Demande du nom de l'évènement
            os.system("mpg123 " + 'sounds/eventSummary.mp3')
            # summary = get_audio()
            summary = input("you :")

            # Demande si il faut ajouter une localisation et si oui, ajoute la localisation
            os.system("mpg123 " + 'sounds/eventLocation.mp3')
            # txt = get_audio()
            txt = input("you :")
            if "oui" in txt:
                txt = txt.split("à")
                location = txt[1].strip()
            else:
                location = "/"

            # Demande si il faut ajouter une description et si oui, l'ajoute
            os.system("mpg123 " + 'sounds/eventDescription.mp3')
            # txt = get_audio()
            txt = input("you :")
            if "oui" in txt:
                description = txt.replace("oui ", "")
            else:
                description = "/"

            # Demande la date du début de l'evènement
            os.system("mpg123 " + 'sounds/dateDebutCalendrier.mp3')
            # txt=get_audio()
            txt = input("you :")
            if "le " in txt.lower():
                txt = txt.replace("le ", "")
                txt = txt.lstrip()
            txt = txt.split(" ")
            mois = moisNbre[txt[1]]
            print(str(txt[0]) + "-" + str(mois) + "-" + str(txt[2]))
            date = str(txt[2]) + "-" + str(mois) + "-" + str(txt[0])

            # Demande l'heure du début de l'évènement
            os.system("mpg123 " + 'sounds/heureDebutCalendrier.mp3')
            # txt=get_audio()
            txt = input("you :")
            if "à" in txt.lower():
                txt = txt.replace("à", "")
                txt = txt.lstrip()
            txt = txt.split("h")
            startDateTime = date + "T" + str(txt[0]) + ":" + str(txt[1]) + ":00-07:00"
            print(startDateTime)

            # Demande l'heure de fin de l'évènement
            os.system("mpg123 " + 'sounds/heureFinCalendrier.mp3')
            # txt=get_audio()
            txt = input("you :")
            if "à" in txt.lower():
                txt = txt.replace("à", "")
                txt = txt.lstrip()
            txt = txt.split("h")
            endDateTime = date + "T" + str(txt[0]) + ":" + str(txt[1]) + ":00-07:00"
            print(endDateTime)

            os.system(
                "python3 calendar/addEvent.py " + summary + " " + location + " " + description + " " + startDateTime
                + " " + endDateTime)
            requestType = "lireCalendrier"

        if "donne-moi les événements du" in commande:
            inp = commande.split()
            longueur = len(rep)
            print('Mois = ' + str(moisNbre[rep[longueur - 1]]))
            print('Jour = ' + rep[longueur - 2])
            os.system("python3 calendar/getEventsDay.py '" + str(rep[longueur - 2]) + '\' \'' + str(
                moisNbre[rep[longueur - 1]]) + '\'')
            # speak("Je recherche les événements du " + )
            # os.system("python3 calendar/getEventsDay.py")
            requestType = "ajouterEvènementsCalendrier"

        if commande == "allume la LED":
            text = 'on'
            os.system("mpg123 " + 'sounds/ledON.mp3')
            requestType = "robot"

        if commande == "éteins la LED":
            text = 'off'
            os.system("mpg123 " + 'sounds/ledOFF.mp3')
            requestType = "robot"

        if commande == "température":
            s.send("temperature")
            data1 = s.recv(1024)
            time.sleep(0.5)
            data2 = s.recv(1024)
            data = data1 + data2
            strg = "Il fait actuellement" + data.decode("utf-8") + "degré dans la pièce"
            speak(strg)
            requestType = "robot"

        if commande == "balade toi":
            s.send("deplacement")
            requestType = "robot"

        if commande == "arrête de te balader":
            s.send("arret")
            requestType = "robot"

        if commande == "tu peux quitter":
            break

        # Lorsqu'une requête est efféctuée, l'humeur est augmentée
        humeurPlus()

        # Envoie du type de requête vers la DB pour la télémétrie
        sql = "INSERT INTO master.request (requestType, requestDate) VALUES ('" + requestType + "', '" + str(
            int(time.time())) + "');"
        cursor = mydb.cursor()
        cursor.execute(sql)
        mydb.commit()
