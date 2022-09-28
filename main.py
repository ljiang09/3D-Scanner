"""
Driver file for calibration curves and sensor visualization.

Generates a sensor calibration curve, validates the curve.
Listens for data from the Arduino scanner, generates a 3D visualization of the scanned object
"""
import serial
import sensor_calibration as calibrate
import python_receive_data as prd

# Link to port for communication with Arduino
arduino_com_port = "/dev/ttyACM0"
baud_rate = 9600   # This value must be the exact same as in the Arduino code
serial_port = serial.Serial(arduino_com_port, baud_rate, timeout=10)

# Calibrate, plot, and fetch parameters of sensor reading vs. distance equation
params = calibrate.run_calibration()

# Fetch data until STOP command given
sensor_volt, positions, radii = prd.fetch_data(serial_port, get_data=True, params=params)

# Generate image of scanned object
prd.plot_heatmap(positions, radii)
