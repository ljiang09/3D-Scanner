
// servo 1 controls the vertical movement, servo 2 controls the horizontal movement
#include <Servo.h>
Servo servo1;
Servo servo2;

// Servos need to be in PWM pins
const int servo1Pin = 3;
const int servo2Pin = 5;
const int sensorPin = A0;


int sensorValue = 0;  // value read in from the sensor
bool positiveRotation = true;  // toggles each time the horizontal servo finishes a pass, so the next pass will be in the opposite direction
const String stopKeyword = "STOP";  // we print this out to the serial port to signal the python code to stop fetching data

// initial positions for the two servos
int pos1 = 0;
int pos2 = 0;

// increments to determine how much each servo will move each time
const int servo1Increment = 4;
const int servo2Increment = 1;


void setup()
{
    long baudRate = 9600;       // NOTE1: The baudRate for sending & receiving programs must match
    Serial.begin(baudRate);     // NOTE2: Set the baudRate to 115200 for faster communication
    servo1.attach(servo1Pin);
    servo2.attach(servo2Pin);
}

void loop()
{
    for (pos1 = 0; pos1 <= 180; pos1 += servo1Increment) {   // in steps of 1 degree, tell servo1 to go to position in variable 'pos1'
        servo1.write(pos1);

        // goes from 0 degrees to 180 degrees
        if (positiveRotation) {
            for (pos2 = 0; pos2 <= 180; pos2 += servo2Increment) {
                servo2.write(pos2);
                sensorValue = analogRead(sensorPin);
                Serial.println(sensorValue + "," + String(pos2) + "," + String(pos1));
                delay(15);
            }
        }

        // goes from 180 degrees to 0 degrees
        else {
            for (pos2 = 180; pos2 >= 0; pos2 -= servo2Increment) {
                servo2.write(pos2);
                sensorValue = analogRead(sensorPin);
                Serial.println(sensorValue + "," + String(pos2) + "," + String(pos1));
                delay(15);
            }
        }

        delay(400);
    }
    
}
