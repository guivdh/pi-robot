import requests
import os
import configparser

cfg = configparser.ConfigParser()
cfg.read('config/config.cfg')

source = cfg.get('news', 'source')


url = ('http://newsapi.org/v2/top-headlines?'
       'country=be&'
       'apiKey=5ff52b90d35b4f91a3eeb532ca66c3a2')

response = requests.get(url)


for i in response.json()['articles']:

    if i['source']['name'] == source:
        string = i['title']
        string = string.replace('"',' ')
        print(string)
        os.system('python3 talking/tts.py \"' + string + '\"')
