import threading
import time

def affiche(nb):
    for i in range(nb):
        time.sleep(1)
    print("Fin du temps")

a = threading.Thread(None, affiche, None, (60,))
a.start()

for i in range(60):
    inp = input("You: ")
    print(inp)