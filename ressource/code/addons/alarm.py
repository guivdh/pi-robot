import time
import threading
import os

def alarme(alarme):
    while True:
        heure = time.localtime()
        print("Heure : " + str(heure[3]) + 'h' + str(heure[4]) + " - Alarme : " + alarme)
        if alarme == str(heure[3]) + 'h' + str(heure[4]):
            os.system("mpg123 ../sounds/alarme.mp3")
            break
        time.sleep(1)

heure = time.localtime()
str(heure[3]) + ':' + str(heure[4])

text = input("you: ")
txt = text.split("à")
print(txt[1].strip())
threadAlarm = threading.Thread(None, alarme, None, (txt[1].strip(),))
threadAlarm.start()
