// Gathers data from IR sensor, prints to Serial Monitor to be read in by a Python listener.

// servo 1 controls the vertical movement, servo 2 controls the horizontal movement
// each servo has a predefined 0 angle. the servo is "centered" at 90 degrees
#include <Servo.h>
Servo servo1;
Servo servo2;

// Note: Servos need to be in PWM pins
const int servo1Pin = 3;
const int servo2Pin = 5;
const int sensorPin = A5;


int sensorValue = 0;  // value read in from the sensor
int sensorAvg = 0; // avg of 10 readings from sensor
bool positiveRotation = true;  // toggles each time the horizontal servo finishes a pass, so the next pass will be in the opposite direction

// initial positions for the two servos
int pos1 = 10;
int pos2 = 30;

// increments to determine how much each servo will move each time
const int servo1Increment = 5;
const int servo2Increment = 1;

// range of motion for each servo
const int servo1Start = 0;
const int servo1End = 25; //25
const int servo2Start = 10; // 10
const int servo2End = 50; //50


// set up servos and communications
void setup()
{
    long baudRate = 9600;       // NOTE1: The baudRate for sending & receiving programs must match
    Serial.begin(baudRate);     // NOTE2: Set the baudRate to 115200 for faster communication
    servo1.attach(servo1Pin);
    servo2.attach(servo2Pin);
}

void loop()
{
   // in steps of 1 degree, tell servo1 to go to position in variable 'pos1'
   for (pos1 = servo1Start; pos1 <= servo1End; pos1 += servo1Increment) {
       // Control the tilt mechanism
       servo1.write(pos1);

       // tells the pan servo to move from 0 degrees to 180 degrees
       if (positiveRotation) {
           for (pos2 = servo2Start; pos2 <= servo2End; pos2 += servo2Increment) {
               // Control the pan mechanism
               servo2.write(pos2);

               // using an average sensor reading reduces "jolting" plots
               sensorAvg = 0;
               for (int i = 0; i < 10; i++) {
                 sensorValue = analogRead(sensorPin);
                 sensorAvg = sensorAvg + sensorValue;
                 delay(50);
               }
               Serial.println(String(sensorAvg/10) + "," + String(pos2) + "," + String(pos1));
               delay(15);

               // if the servo has reached the end of its pass, toggle variable so it moves in the opposite direction
               if (pos2 == servo2End) {
                   positiveRotation = false;
               }
           }
       }

       // tells the pan servo to move from 180 degrees to 0 degrees
       else {
           for (pos2 = servo2End; pos2 >= servo2Start; pos2 -= servo2Increment) {
               // Control the pan mechanism
               servo2.write(pos2);
               sensorValue = analogRead(sensorPin);
               
               // using an average sensor reading reduces "jolting" plots
               sensorAvg = 0;
               for (int i = 0; i < 10; i++) {
                  sensorValue = analogRead(sensorPin);
                  sensorAvg = sensorAvg + sensorValue;
                  delay(50);
               }
               Serial.println(String(sensorAvg/10) + "," + String(pos2) + "," + String(pos1));
               delay(15);

               // if the servo has reached the end of its pass, toggle variable so it moves in the opposite direction
               if (pos2 == servo2Start) {
                   positiveRotation = true;
               }
           }
       }

       delay(400);
   }

   // STOP is the keyword to signal the python code to stop fetching data
   Serial.println("STOP");
    
}
