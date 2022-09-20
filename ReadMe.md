# Mini-Project 2: DIY 3D Scanner

## Objectives

1. Build and program a rudimentary 3D scanner using a pan/tilt mechanism
2. Scan an object of known, well-defined geometry
3. Visualize the output from your scanner

## Testing the parts
Before delving into anything, each of the parts needed to be tested for functionality.

### Sensor:
The sensor used in this project was the [Sharp GP2Y0A02YK0F IR distance sensor](https://www.pololu.com/file/0J156/gp2y0a02yk_e.pdf).

The Arduino IDE comes with an example called "AnalogInput", which we used to test that the sensor readings changed with distance as expected.

### Motors:
We used the [Tiankongrc MG996R servo motors](https://components101.com/motors/mg996r-servo-motor-datasheet).

The Arduino IDE comes with an example called “Sweep”, which causes a servo to rotate back and forth.
This checks to make sure the motor responds to commands properly, and actually rotates a full 180 degrees.


Requirements:

A description of the process you used to test your sensor
A calibration plot depicting analog voltage reading vs. actual distance
An error plot showing predicted distance and actual distance for distances not included in your calibration routine
An explanation of your calibration function
An image of your setup for the 1 servo scan of your letter and the data depicting the top view
An image of your setup for the 2 servo apparatus and visualization of the 3D data resulting from your scan (a plot, an image, a video, etc)
An explanation of and reflection on your design (including software, electrical and mechanical parts). What worked well and what could be improved?
All source code


