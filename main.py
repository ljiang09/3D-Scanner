"""
Driver file for calibration curves and sensor visualization.

Generates a sensor calibration curve, validates the curve.
Listens for data from the Arduino scanner, generates a 3D visualization of the scanned object
"""
import serial
import sensor_calibration as calibrate
import python_receive_data as prd

# Link to port for communication with Arduino
ARDUINO_COM_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600   # This value must be the exact same as in the Arduino code
SERIAL_PORT = serial.Serial(ARDUINO_COM_PORT, BAUD_RATE, timeout=10)

# Calibrate, plot, and fetch parameters of sensor reading vs. distance equation
PARAMS = calibrate.run_calibration()

# Fetch data until STOP command given
SENSOR_VOLT, POSITIONS, RADII = prd.fetch_data(SERIAL_PORT, get_data=True, params=PARAMS)

# Generate image of scanned object
prd.plot_heatmap(POSITIONS, RADII)
