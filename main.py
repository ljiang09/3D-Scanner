"""
TODO:
"""
import serial
import sensor_calibration as calibrate
import python_receive_data as prd

# Link to port
arduino_com_port = "/dev/ttyACM0"
baud_rate = 9600
serial_port = serial.Serial(arduino_com_port, baud_rate, timeout=10)

# Calibrate, plot, and fetch parameters of equation
params = calibrate.run_calibration()

# Fetch data until STOP command given
sensor_volt, positions, radii = prd.fetch_data(serial_port, get_data=True, params=params)

# Generate image of object
prd.plot_heatmap(positions, radii)