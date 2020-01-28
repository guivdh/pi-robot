import bluetooth

serverMACAddress = '98:D3:33:F5:AE:4D'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
print("Entrez ON pour allumer la led")
print("Entrez OFF pour éteindre la led")
print("Entrez quit pour arrêter le programme")
while 1:
    text = input("--> ") # Note change to the old (Python 2) raw_input
    if text == "quit":
        break
    s.send(text)
