import requests
import os
import configparser

cfg = configparser.ConfigParser()
#cfg.read('config/config.cfg')

#source = cfg.get('news', 'source')


url = ('https://prevision-meteo.ch/services/json/bruxelles-1')

response = requests.get(url)

ville = result = ''.join([i for i in response.json()['city_info']['name'] if not i.isdigit()])
temperature = response.json()['current_condition']['tmp']
condition = response.json()['current_condition']['condition']

string = "Actuellement à " + ville + ", il fait " + str(temperature) + " degré et un temps " + condition
print(string)

#os.system('python3 talking/tts.py \"' + string + '\"')