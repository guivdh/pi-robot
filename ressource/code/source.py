import os
import time
import speech_recognition as sr
import bluetooth
from gtts import gTTS
import sys
from mutagen.mp3 import MP3
from time import sleep
from playsound import playsound

serverMACAddress = '98:D3:33:F5:AE:4D'
port = 1

try:
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((serverMACAddress, port))
except Exception as e:
    print("Exception : " + str(e))
    print("Une erreur est survenue")
    audio = MP3("sounds/erreur.mp3")
    player = os.system("mpg123 "+"sounds/erreur.mp3")
    sleep(audio.info.length+1)
    sys.exit()


def speak(text):
    tts = gTTS(text=text, lang='fr')
    filename="voice.mp3"
    tts.save(filename)
    os.system("mpg123 "+'voice.mp3')


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
    commande = input()
    if commande == "Salut":
        player = os.system("mpg123 "+'sounds/caVa?.mp3')
        commande = input()
        player = os.system("mpg123 "+'sounds/boomer.mp3')
    if commande == "allume la LED":
        text = 'on'
        os.system("mpg123 "+'sounds/ledON.mp3')
    if commande == "éteins la LED":
        text = 'off'
        os.system("mpg123 "+'sounds/ledOFF.mp3')
    if commande == "donne-moi la température":
        text = 'temperature'
    if commande == "quitter":
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
