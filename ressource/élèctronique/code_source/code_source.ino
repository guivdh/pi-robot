#include <SoftwareSerial.h>   // librairie pour creer une nouvelle connexion serie max 9600 baud
#include <dht11.h>
#include <Servo.h>

SoftwareSerial BTSerial(10, 11); // RX | TX  = > BT-TX=10 BT-RX=11

#define DHT11PIN 8
dht11 DHT11;
String mot;
int temp;
char str[2];

int dev = 1;

float distanceObstacle = 0;

int IN1=7;
int IN2=12;
int IN3=13;
int IN4=5;
int ENB=6;

int pinTrig = 52;
int pinEcho = 53;
long temps;
float distance;


Servo monServomoteur1;
Servo monServomoteur2;
Servo monServomoteur3;

int ledR = 3;
int ledB = 2;
int ledG = 4;

int cam = 35;

void setup()
{

  pinMode(pinTrig, OUTPUT);
  pinMode(pinEcho, INPUT);
  digitalWrite(pinTrig, LOW); 

  monServomoteur1.attach(22);
  monServomoteur2.attach(23);
  monServomoteur3.attach(24);

  //bras en bas du robot
  monServomoteur2.write(140);
  monServomoteur3.write(7);

  //radar au milieu
  monServomoteur1.write(62);


  //Moteurs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  
  analogWrite(ENB, 110); //110

  digitalWrite(ledR, LOW); 
  digitalWrite(ledG, LOW); 
  digitalWrite(ledB, LOW); 
  
  Serial.begin(9600);
  Serial.println("Enter a command:");
  BTSerial.begin(9600);  // HC-05 9600 baud


}

void loop()
{

   if(dev==0){
    String text = getBluetooth();
    if(text != ""){

      if(text == "salutation"){
        bonjour();
      }
      if(text == "temperature"){
        getTemperature();
      }
      if(text == "avance"){
        deplacement();
        while(true){
          distanceObstacle = mesureDistance();
          text = getBluetooth();
          if(text != ""){
            Serial.println(text);  
          }
          
          if(text == "arret"){
            arret();
            break;
          }
          if(distanceObstacle < 15){
            arret();
            break;
          }
        }
      }
      if(text == "arret"){
        arret();
      }
      

      /*
       * fonction qui détermine la couleur des yeux lorsque la commande est "couleur-255-255-255 
       */
      if(text.indexOf("couleur")>=0){
        char phrase[50];
        const char s[2] = "-";
        char *token;
        int i=0;
        char *rgb[4];

        text.toCharArray(phrase,50);
        token = strtok(phrase, s);
        while( token != NULL){
          rgb[i] = token;
          token = strtok(NULL,s);
          i++;
        }
        if(atoi(rgb[1]) <= 0 || atoi(rgb[2]) >= 255){
          setColor(0,255,0);
        }
        else{
          setColor(atoi(rgb[1]),atoi(rgb[2]),atoi(rgb[3]));
        }
        
      }
      /*
       * 
       */
      Serial.println(text);
      
    }
   }
   else if(dev==1){
    delay(2000);
     Serial.println("Phase de développement");
     tourneDroite();
     heureux(8);
     arret();
     
     for (;;);
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
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
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
  return distance;
}

void setColor(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(ledR, red_light_value);
  analogWrite(ledG, green_light_value);
  analogWrite(ledB, blue_light_value);
}

void reveil(){
  monServomoteur2.write(7);
  monServomoteur3.write(140);
  delay(250);
  monServomoteur2.write(37);
  monServomoteur3.write(110);
  delay(250);
  monServomoteur2.write(7);
  monServomoteur3.write(140);
  delay(250);
  monServomoteur2.write(140);
  monServomoteur3.write(7);
}

void heureux(int nbr){
  for(int i=0;i<nbr;i++){
  monServomoteur2.write(37);
  monServomoteur3.write(140);
  delay(200);
  monServomoteur2.write(7);
  monServomoteur3.write(110);
  delay(200);
  }
  monServomoteur2.write(140);
  monServomoteur3.write(7);
}

void bonjour(){
  for(int i=0;i<5;i++){
  monServomoteur2.write(0);
  delay(250);
  monServomoteur2.write(37);
  delay(250);
  }
  monServomoteur2.write(140);
}

void aleatoire(){
  int pos1=0;
  int pos2=0;
  int color1=0;
  int color2=0;
  int color3=0;
  for(int i=0;i<5;i++){
    pos1 = random(0,120);
    pos2 = random(7,140);
    color1 = random(0,255);
    color2 = random(0,255);
    color3 = random(0,255);
    Serial.println(pos1);
    Serial.println(pos2);
    monServomoteur2.write(pos1);
    monServomoteur3.write(pos2);
    setColor(color1,color2,color3);
    delay(300);
    
  }
}

void yeux(){
  for(int i=0;i<255;i++){
    setColor(i,255-i,0);
    delay(50);
  }
  for(int i=255;i>0;i--){
    setColor(i,255-i,255-i);
    delay(50);
  }
}

String getBluetooth(){
      String message;
      while (BTSerial.available()){
      // Lecture du message envoyé par le BT
      // Read message send by BT
      message = BTSerial.readString();
      // Ecriture du message dans le serial usb
      // write in serial usb
      //Serial.println(message);
    }
    return message;
}

void tourneDroite(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void tourneGauche(){
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}
