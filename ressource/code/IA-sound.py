import json
import os

with open("IA-conversation/json file/intents.json") as json_file:
    data = json.load(json_file)
    for p in data['intents']:
        tag = p['tag']
        i = 0
        for a in p['responses']:
            tag = tag.replace(" ", "-")
            os.system("python3 ajouterSon.py \""+a+"\" \""+tag+"-"+str(i)+"\"")
            i+=1