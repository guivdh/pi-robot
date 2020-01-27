import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from mutagen.mp3 import MP3

def speak(mot):
    tts = gTTS(text=mot, lang='fr')
    filename = "voice.mp3"
    tts.save(filename)

    audio = MP3(filename)
    player = OMXPlayer(filename, args=['-o', 'local'])
    sleep(audio.info.length)
    player.quit()

    os.remove('voice.mp3')

def get_audio():
    r = sr.Recognizer()
    print('En écoute !')
    OMXPlayer("Windows Pop-up Blocked.wav", args=['-o', 'local'])
    mic = sr.Microphone()
    with mic as source:
        audioSon = r.listen(source)
        OMXPlayer("Windows Balloon.wav", args=['-o', 'local'])
        said = ""

        try:
            said = r.recognize_google(audioSon, language='fr-FR')
            print(said)
        except Exception as e:
            print("Exception : " + str(e))
            speak("Une erreur est survenue")
    return said


speak("Bonjour, que puis-je faire pour vous?")
print("Bonjour, que puis-je faire pour vous?")

text = ""
while("répète" not in text) :
    text = get_audio()

while("arrête" not in text) :
    text = get_audio()
    if("arrête" in text) :
        print("Ok, j'arrête de répéter!")
    else :
        speak(text)
