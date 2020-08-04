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


while 1:
    text = input("--> ")
    if text == "on":
        print('Led allumée')
    if text == "off":
        print('Led éteinte')
    if text == "quit":
        break
    s.send(text)
