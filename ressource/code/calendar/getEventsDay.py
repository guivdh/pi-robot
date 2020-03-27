from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gtts import gTTS
import sys

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

mois={1:'janvier',2:'février',3:'mars',4:'avril',5:'mai',6:'juin',7:'juillet',8:'août',9:'septembre',10:'octobre',11:'novembre',12:'décembre'}

"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""

def speak(text):
    tts = gTTS(text=text, lang='fr')
    filename="voice.mp3"
    tts.save(filename)
    os.system("mpg123 "+'voice.mp3')

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')

    date1 = datetime.datetime(2020, int(sys.argv[2]), int(sys.argv[1]))

    # Date time separator is a "#" symbol
    min=(date1.isoformat())

    date2 = datetime.datetime(2020, int(sys.argv[2]), int(sys.argv[1]),23,59,59)

    # Date time separator is a "#" symbol
    max=(date2.isoformat())
    print(now)
    print(min)
    print(max)



    events_result = service.events().list(calendarId='primary', timeMin=min+'Z', timeMax = max+'Z', singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Aucun évènement à venir.')
        player = os.system("mpg123 "+'sounds/aucunEvenementJour.mp3')

    nbrEvent = 0

    for i in events:
        nbrEvent = nbrEvent + 1
    strg = "Vous avez " + str(nbrEvent) + "évènements le " + str(int(sys.argv[1])) + mois[int(sys.argv[2])]
    speak(strg)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        print(event['summary'])
        print("mois : " + start[5:7])
        print("Jour : " + start[8:10])
        strg = event['summary'] + " le " + start[8:10] + " " + mois[int(start[5:7])]
        print(strg)
        speak(strg)

main()
