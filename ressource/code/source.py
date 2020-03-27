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


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    print(now)
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Aucun évènement à venir.')
        player = os.system("mpg123 "+'sounds/aucunEvenement.mp3')

    nbrEvent = 0

    for i in events:
        nbrEvent = nbrEvent + 1
    strg = "Vous avez " + str(nbrEvent) + "évènements à venir"
    speak(strg)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        print(event['summary'])
        print("mois : " + start[5:7])
        print("Jour : " + start[8:10])
        strg = event['summary'] + " le " + start[8:10] + " " + mois[int(start[5:7])]
        print(strg)
        speak(strg)




player = os.system("mpg123 "+'sounds/actionChoix.mp3')

while 1:

    text = ""
    commande = get_audio()
    if commande == "Salut":
        player = os.system("mpg123 "+'sounds/caVa?.mp3')
    if commande == "donne-moi les événements à venir":
        player = os.system("mpg123 "+'sounds/rechercheCalendrier.mp3')
        main()
    if commande == "allume la LED":
        text = 'on'
        os.system("mpg123 "+'sounds/ledON.mp3')
    if commande == "éteins la LED":
        text = 'off'
        os.system("mpg123 "+'sounds/ledOFF.mp3')
    if commande == "donne-moi la température":
        text = 'temperature'
    if commande == "quitter":
        # Local time without timezone information printed in ISO 8601 format
        dateTime = datetime.datetime.today()

        # Date time separator is a "#" symbol
        print(dateTime.isoformat("T"))
        break

    s.send(text)

    if text == 'temperature':
        s.close()
        server_socket = bluetooth.BluetoothSocket(RFCOMM)
        server_socket.bind(("", 3 ))
        server_socket.listen(1)

        s, address = server_socket.accept()

        data = client_socket.recv(1024)

        print(data)

        server_socket.close()


        #print('Il fait ' + stringdata + ' degré dans la pièce')
