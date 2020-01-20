import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
#from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from mutagen.mp3 import MP3

def speak(mot):
    tts = gTTS(text=mot, lang='fr')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    #sound_path = Path(filename)
    audio = MP3(filename)
    #player = OMXPlayer(sound_path)
    sleep(audio.info.length)

    #player2=OMXPlayer(sound_path)
    #sleep(audio.info.length)
    #player.quit()
    #player2.quit()
    os.remove('voice.mp3')

def get_audio():
    r = sr.Recognizer()
    print('En écoute !')
    playsound.playsound("Windows Pop-up Blocked.wav")
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language='fr-FR')
            print(said)
        except Exception as e:
            print("Exception : " + str(e))
            speak("Une erreur est survenue")
    return said


speak("Bonjour")
text = ""
while("répète" not in text) :
    text = get_audio()

while("stop" not in text) : 
    text = get_audio()
    if("stop" in text) :
        speak("Ok, j'arrête de répéter!")
    else :
        speak(text)
