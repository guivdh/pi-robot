#include <SoftwareSerial.h>   // librairie pour creer une nouvelle connexion serie max 9600 baud
#define PIN_LED 22

SoftwareSerial BTSerial(10, 11); // RX | TX  = > BT-TX=10 BT-RX=11

void setup()
{
  Serial.begin(9600);
  Serial.println("Enter a command:");
  BTSerial.begin(9600);  // HC-05 9600 baud 

  pinMode(PIN_LED, OUTPUT);
}

void loop()
{
  String message;
    // Boucle de lecture sur le BT
    // Reading BT
    while (BTSerial.available()){
      // Lecture du message envoyé par le BT
      // Read message send by BT
      message = BTSerial.readString();
      // Ecriture du message dans le serial usb
      // write in serial usb
      Serial.println(message);
    }
    // Boucle de lecture sur le serial usb
    // Reading serial usb
    while (Serial.available()){
      // Lecture du message envoyé par le serial usb
      // Read message send by serial usb
      message = Serial.readString();
      // Ecriture du message dans le BT
      // write in BT 
      BTSerial.println(message);
    }

  // si mon message est egal a "on"  ( + retour chariot et nouvelle ligne )
  // if message equal to "on" (+ carriage return and newline )
    if(message == "on"){
      digitalWrite(PIN_LED,HIGH); // led on
    }// else if message off
    else if(message == "off"){
      digitalWrite(PIN_LED,LOW);  // led off
    }
}
