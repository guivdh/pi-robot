import threading
import time

def affiche(nb):
    for i in range(nb):
        time.sleep(1)
    print("Fin du temps")


def humeur():
    print("thread")
    while True:
        nbr = ""
        f = open("../config/data.txt", "r")
        txt = f.read()
        data = txt.split("=")
        nbr = int(data[1])
        newNbr = nbr - 1
        print(newNbr)
        a = open("../config/data.txt", "w")
        string = "humeur="+str(newNbr)
        a.write(string)
        f.close()
        a.close()
        time.sleep(2)

humeur = threading.Thread(None, humeur, None, ())
humeur.start()