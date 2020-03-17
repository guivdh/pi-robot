import os
import time
import playsound
import bluetooth
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import sys

serverMACAddress = '98:D3:33:F5:AE:4D'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
try:
    s.connect((serverMACAddress, port))
except Exception as e:
    print("Exception : " + str(e))
    print("Une erreur est survenue")
    playsound("sounds/erreur.mp3")
    sys.exit()


def speak(text):
    tts = gTTS(text=text, lang='fr')
    filename="voice.mp3"
    tts.save(filename)
    playsound('voice.mp3')

playsound('sounds/actionChoix.mp3')


def get_audio():
    r = sr.Recognizer()
    print('En écoute !')
    playsound("sounds/Windows Pop-up Blocked.wav")
    mic = sr.Microphone()
    with mic as source:
        audioSon = r.listen(source)
        playsound("sounds/Windows Balloon.wav")
        said = ""

        try:
            said = r.recognize_google(audioSon, language='fr-FR')
            print(said)
        except Exception as e:
            print("Exception : " + str(e))
            playsound("sounds/erreur.mp3")
    return said


while 1:
    text = ""
    commande = get_audio()
    if commande == "allume la LED":
        text = 'on'
        playsound('sounds/ledON.mp3')
    if commande == "éteins la LED":
        text = 'off'
        playsound('sounds/ledOFF.mp3')
    if commande == "donne-moi la température":
        text = 'temperature'
    if commande == "quitter":
        break

    s.send(text)

    if text == 'temperature':
        data = s.recv(1024)
        stringdata = data.decode('utf-8')
        print('Il fait ' + stringdata + ' degré dans la pièce')
