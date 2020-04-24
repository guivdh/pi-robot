#include <SoftwareSerial.h>   // librairie pour creer une nouvelle connexion serie max 9600 baud
#include <dht11.h>
#define PIN_LED 7
#include <Servo.h>

SoftwareSerial BTSerial(10, 11); // RX | TX  = > BT-TX=10 BT-RX=11

#define DHT11PIN 8
dht11 DHT11;
String mot;
int temp;
char str[2];

int IN1=2;
int IN2=3;
int IN3=4;
int IN4=5;
int ENB=6;

int pinTrig = 52;
int pinEcho = 53;
long temps;
float distance;

Servo monServomoteur;


void setup()
{

  pinMode(pinTrig, OUTPUT);
  pinMode(pinEcho, INPUT);
  digitalWrite(pinTrig, LOW); 

  monServomoteur.attach(51);
  
  Serial.begin(9600);
  Serial.println("Enter a command:");
  BTSerial.begin(9600);  // HC-05 9600 baud

  pinMode(PIN_LED, OUTPUT);

  //Moteurs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  
  analogWrite(ENB, 255);
  analogWrite(ENB, 130); //130


}

void loop()
{

  // Fait bouger le bras de 0° à 180°
  monServomoteur.write(62); //aligne le capteur devant
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

  // si mon message est egal a "on"  ( + retour chariot et nouvelle ligne )
  // if message equal to "on" (+ carriage return and newline )
    if(message == "on"){
      digitalWrite(PIN_LED,HIGH); // led on
    }// else if message off
    else if(message == "off"){
      digitalWrite(PIN_LED,LOW);  // led off
    }
    else if(message == "temperature"){
      getTemperature();
    }
    else if(message == "deplacement"){
      deplacement();
      while(true){
        if(mesureDistance()<10){
          arret();
        }
        while (BTSerial.available()){
          // Lecture du message envoyé par le BT
          // Read message send by BT
          message = BTSerial.readString();
          // Ecriture du message dans le serial usb
          // write in serial usb
          Serial.println(message);
        }

        delay(200);  
      }  
    }
    else if(message == "arret"){
      arret();
    }
}


void getTemperature() {
  int temperature = 0;
  int humidity = 0;
  int chk = DHT11.read(DHT11PIN);

  Serial.print((int)DHT11.temperature);
  Serial.print("°C, ");
  Serial.print((int)DHT11.humidity);
  Serial.println("%");
  sprintf(str, "%d", DHT11.temperature);
  Serial.print("Donnée envoyée : ");
  Serial.println(str);
  BTSerial.write(str);
}

void deplacement(){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void arret(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

float mesureDistance(){
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);  
  distance = pulseIn(pinEcho, HIGH) / 58.0; 
  Serial.println(distance);
  return distance;
}
