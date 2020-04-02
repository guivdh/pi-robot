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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

mois={1:'janvier',2:'février',3:'mars',4:'avril',5:'mai',6:'juin',7:'juillet',8:'août',9:'septembre',10:'octobre',11:'novembre',12:'décembre'}
moisNbre={'janvier':1,'février':2,'mars':3,'avril':4,'mai':5,'juin':6,'juillet':7,'août':8,'septembre':9,'octobre':10,'novembre':11,'décembre':12}

serverMACAddress = '98:D3:33:F5:AE:4D'
port = 1

def speak(text):
    tts = gTTS(text=text, lang='fr')
    filename="voice.mp3"
    tts.save(filename)
    os.system("mpg123 "+'voice.mp3')

def speakEnglish(text):
    tts = gTTS(text=text, lang='en')
    filename="voice.mp3"
    tts.save(filename)
    os.system("mpg123 "+'voice.mp3')

#Connection au bluetooth
try:
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((serverMACAddress, port))
except Exception as e:
    print("Exception : " + str(e))
    print("Une erreur est survenue")
    audio = MP3("sounds/erreur.mp3")
    player = os.system("mpg123 "+"sounds/erreur.mp3")
    speakEnglish(str(e))
    sys.exit()

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

player = os.system("mpg123 "+'sounds/actionChoix.mp3')

while 1:

    text = ""
    commande = get_audio()
    if commande == "Salut":
        player = os.system("mpg123 "+'sounds/caVa.mp3')

    if commande == "donne-moi les événements à venir":
        player = os.system("mpg123 "+'sounds/rechercheCalendrier.mp3')
        os.system("python3 calendar/getEvents.py")

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


    if commande == "quitter":
        # Local time without timezone information printed in ISO 8601 format
        date1 = datetime.datetime(1996, 12, 11)

        # Date time separator is a "#" symbol
        min=(date1.isoformat("T"))
        print(min)
        break


    s.send(text)


        #print('Il fait ' + stringdata + ' degré dans la pièce')
