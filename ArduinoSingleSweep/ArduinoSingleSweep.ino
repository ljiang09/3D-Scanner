// servo 1 controls the vertical movement, servo 2 controls the horizontal movement
// each servo has a predefined 0 angle. the servo is "centered" at 90 degrees
#include <Servo.h>
Servo servo1;
Servo servo2;

// Servos need to be in PWM pins
const int servo1Pin = 3;
const int servo2Pin = 5;
const int sensorPin = A5;


int sensorValue = 0;  // value read in from the sensor
int sensorAvg = 0; // avg of 10 readings from sensor

// initial positions for the two servos
int pos1 = 10;
int pos2 = 30;

// increments to determine how much each servo will move each time
const int servo2Increment = 1;

// range of motion for each servo
const int servo2Start = 10; // 10
const int servo2End = 50; //50


void setup()
{
    long baudRate = 9600;       // NOTE1: The baudRate for sending & receiving programs must match
    Serial.begin(baudRate);     // NOTE2: Set the baudRate to 115200 for faster communication
    servo1.attach(servo1Pin);
    servo2.attach(servo2Pin);
}


void loop() {
  // move servo 1 (tilting) to face directly forward and stay there
  servo1.write(pos1);

  // sweep servo 2 (panning) through one pass
  for (pos2 = servo2Start; pos2 <= servo2End; pos2 += servo2Increment) {
      servo2.write(pos2);
      sensorAvg = 0;
      for (int i = 0; i < 10; i++) {
        sensorValue = analogRead(sensorPin);
        sensorAvg = sensorAvg + sensorValue;
        delay(50);
      }
      // print distance and angle values to the serial monitor for python parsing
      Serial.println(String(sensorAvg/10) + "," + String(pos2) + "," + String(pos1));
    
  }
}
