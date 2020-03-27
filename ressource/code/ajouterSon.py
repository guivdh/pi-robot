import os
import time
import bluetooth
import speech_recognition as sr
from gtts import gTTS
from mutagen.mp3 import MP3
import sys
from time import sleep

def speak(text,file):
    tts = gTTS(text=text, lang='fr')
    filename="sounds/"+file+".mp3"
    tts.save(filename)
    print(filename)
    os.system("mpg123 "+filename)
    sys.exit()

mot = sys.argv[1]
file = sys.argv[2]
speak(mot,file)
