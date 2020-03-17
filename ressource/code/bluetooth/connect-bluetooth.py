import os
import time
import playsound
import bluetooth
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS

serverMACAddress = '98:D3:33:F5:AE:4D'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))

def speak(text):
    tts = gTTS(text=text, lang='fr')
    filename="voice.mp3"
    tts.save(filename)
    playsound('voice.mp3')

speak('    Sélectionner l action à faire')

while 1:
    text = input("--> ")
    if text == "on":
        speak('Led allumée')
    if text == "off":
        speak('Led éteinte')
    if text == "quit":
        break
    s.send(text)
