import os
import time
import playsound
import bluetooth
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import sys

def speak(text,file):
    tts = gTTS(text=text, lang='fr')
    filename="sounds/"+file+".mp3"
    tts.save(filename)
    playsound('sounds/'+file+'.mp3')

mot = sys.argv[1]
file = sys.argv[2]
speak(mot,file)
