//      ******************************************************************
//      *                                                                *
//      *                                                                *
//      *     Example Arduino program that transmits data to a laptop    *
//      *                                                                *
//      *                                                                *
//      ******************************************************************


// initialize hardware and software. Servos need to be in PWM pins

// servo 1 controls the vertical movement, servo 2 controls the horizontal movement
#include <Servo.h>
Servo servo1;
Servo servo2;

const int servo1Pin = 3;
const int servo2Pin = 5;
const int sensorPin = A0;

int sensorValue = 0;  // value read in from the sensor
int pos1 = 0;
int pos2 = 0;

// these increments determine how much each servo will move between collecting data
const int servo1Increment = 4;
const int servo2Increment = 1;

// toggles each time the horizontal servo reaches the end of its pass, so the next pass will be in the opposite direction
bool positiveRotation = true;

const String stopKeyword = "STOP";  // we print this out to the serial port to signal the python code to stop fetching data

void setup()
{
  long baudRate = 9600;       // NOTE1: The baudRate for sending & receiving programs must match
  Serial.begin(baudRate);     // NOTE2: Set the baudRate to 115200 for faster communication
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
}

void loop()
{
    for (pos1 = 0; pos1 <= 20; pos1 += servo1Increment) {   // control servo 1
        
        // in steps of 1 degree, tell servo1 to go to position in variable 'pos1'
        servo1.write(pos1);

        // goes from 0 degrees to 180 degrees
        if (positiveRotation) {
            for (pos2 = 0; pos2 <= 20; pos2 += servo2Increment) {
                servo2.write(pos2);
                sensorValue = analogRead(sensorPin);
                Serial.println(sensorValue);
                delay(15);
            }
        }

        // goes from 180 degrees to 0 degrees
        else {
            for (pos2 = 20; pos2 >= 0; pos2 -= servo2Increment) {
                servo2.write(pos2);
                sensorValue = analogRead(sensorPin);
                Serial.println(sensorValue);
                delay(15);
            }
        }

        delay(400);
    }
    
}
