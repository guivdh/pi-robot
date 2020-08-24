# -*- coding: utf-8 -*-

import requests
import random
import sys
import os

i = random.randint(1,114)

x = requests.get('https://bridge.buddyweb.fr/api/blagues/blagues/'+str(i))

txt = x.json()

print(txt["blagues"])

blague = txt["blagues"].replace("\"", " ")

os.system("python3 talking/tts.py \"" + blague + "\"")
