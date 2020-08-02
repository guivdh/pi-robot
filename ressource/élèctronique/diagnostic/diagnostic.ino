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


Servo monServomoteur1;
Servo monServomoteur2;
Servo monServomoteur3;

int ledR = 31;
int ledB = 29;
int ledG = 33;

int cam = 35;


void setup()
{
  
  pinMode(pinTrig, OUTPUT);
  pinMode(pinEcho, INPUT);
  digitalWrite(pinTrig, LOW); 

  monServomoteur1.attach(22);
  monServomoteur2.attach(23);
  monServomoteur3.attach(24);

  monServomoteur2.write(180);
  monServomoteur3.write(180);
  
  Serial.begin(9600);
  Serial.println("Initialisation du programme");
  
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

  digitalWrite(ledR, LOW); 
  digitalWrite(ledG, LOW); 
  digitalWrite(ledB, LOW); 


}

void loop()
{

  Serial.println("Diagnostic en cours");
  delay(1000);
  /*Serial.println("1 - Servomoteur");
  servomoteur();
  delay(2000);

  Serial.println("\n2 - Température (DHT11)");
  getTemperature();
  delay(2000),
  
  Serial.println("\n3 - Mesure distance");
  mesureDistance();
  delay(2000);
  

  Serial.println("\n4 - LED RGB");
  setColor(255,0,0);
  delay(1000);
  setColor(0,255,0);
  delay(1000);
  setColor(0,0,255);
  delay(1000);
  setColor(255,255,255);*/

  while(1){
    Serial.println(digitalRead(9));
    delay(200);
  }

  //Serial.println("\n5 - Caméra");
  //analogWrite(cam, 255);
  /*
  digitalWrite(ledR, LOW); 
  digitalWrite(ledG, LOW); 
  digitalWrite(ledB, LOW);*/
  
  /*Serial.println("\n4 - Avance");
  avancer();
  delay(2000);

  Serial.println("\n5 - Recule");
  reculer();
  delay(2000);

  Serial.println("\n6 - Arrêt");
  arret();
  delay(2000);*/

  

  Serial.println("Diagnostic terminé");
  
  while(true){
    delay(1000);
  }
}

void servomoteur(){
  // Fait bouger le bras de 0° à 180°
  Serial.println("Servomoteur 1");
  monServomoteur1.write(42);
  delay(1000);
  monServomoteur1.write(82);
  delay(1000);
  monServomoteur1.write(62);
  delay(1000);
  
  Serial.println("Servomoteur 2");

  monServomoteur2.write(0);
  delay(1000);
  monServomoteur2.write(180);
  delay(1000);

  Serial.println("Servomoteur 3");

  monServomoteur3.write(0);
  delay(1000);
  monServomoteur3.write(180);
  delay(1000);

}


void getTemperature() {
  int temperature = 0;
  int humidity = 0;
  int chk = DHT11.read(DHT11PIN);

  Serial.print((int)DHT11.temperature);
  Serial.print("°C, ");
  Serial.print((int)DHT11.humidity);
  Serial.println("%");
}

void avancer(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void reculer(){
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

void setColor(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(ledR, red_light_value);
  analogWrite(ledG, green_light_value);
  analogWrite(ledB, blue_light_value);
}
