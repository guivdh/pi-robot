"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""

import bluetooth
import time

serverMACAddress = '98:D3:33:F5:AE:4D'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = input('$') # Note change to the old (Python 2) raw_input
    if text == "quit":
        break

    if text == "server":
        s.send("temperature")
        data1 = s.recv(1024)
        time.sleep(0.5)
        s.send("temperature")
        data2 = s.recv(1024)
        data = data1+data2
        print("Température : ",data.decode("utf-8"))

    #s.send(text)
s.close()
