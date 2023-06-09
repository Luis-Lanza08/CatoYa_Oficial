/*
  Arduino Slave for Raspberry Pi Master
  i2c_slave_ard.ino
  Connects to Raspberry Pi via I2C
  
  DroneBot Workshop 2019
  https://dronebotworkshop.com
*/
 
// Include the Wire library for I2C
#include <Wire.h>
 
// LED on pin 13
const int ledPin = 13; 
const int alimentacion = 3; 
byte contador = 0;
int cadena[3];

int p = 0; // sino
int q = 0; // valor1 
int r = 0; // valor2

// pines del motor para controlar velocidad
int motor_izquierda = 6; //pwm
int motor_derecha = 5; //pwm

//pines del motor para controlar sentido de giro
int pin_motor_izquierda1 = 8;
int pin_motor_izquierda2 = 9;

int pin_motor_derecha1 = 10;
int pin_motor_derecha2 = 11;


// hiperametros
int velocidad_inicial = 150;
int error_serial =0; // dato que vendra de python




void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x30);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);

  
  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  digitalWrite(alimentacion, HIGH);
 // Serial.begin(9600);

  // declaracion de pines para PWM
  pinMode(motor_izquierda, OUTPUT);
  pinMode(motor_derecha, OUTPUT);
  // declaracion de pines para giro del motor
  pinMode(pin_motor_izquierda1, OUTPUT);
  pinMode(pin_motor_izquierda2, OUTPUT);
  pinMode(pin_motor_derecha1, OUTPUT);
  pinMode(pin_motor_derecha2, OUTPUT); 


      
  digitalWrite(pin_motor_izquierda1, HIGH);
  digitalWrite(pin_motor_izquierda2, LOW);

    digitalWrite(pin_motor_derecha1, LOW);
    digitalWrite(pin_motor_derecha2, HIGH);  
  
}
 
// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
     p = Wire.read(); // receive byte as a character
  //  Serial.println(p);
    //if(Wire.available()){
       q = Wire.read();
      // Serial.println(q);
    //}
    //if(Wire.available()){
       r = Wire.read();
      //Serial.println(r);
    //}
    int dato = (q*256)+r;
    if(p == 0){
      dato = dato*(-1);
    }
    error_serial = dato;
    //Serial.println(dato);
       //establecer velocidad de giro en base a los datos obtenidos
    //analogWrite(motor_izquierda, (velocidad_inicial-error_serial));
    analogWrite(motor_derecha, (velocidad_inicial + error_serial));
    analogWrite(motor_izquierda, (velocidad_inicial - error_serial));


  }
}
void loop() {
  

}