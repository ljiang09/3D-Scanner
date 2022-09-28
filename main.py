"""
TODO:
"""
import serial
import sensor_calibration as calibrate
import python_receive_data as prd

# Link to port
arduino_com_port = "/dev/ttyACM1"
baud_rate = 9600
serial_port = serial.Serial(arduino_com_port, baud_rate, timeout=10)

# Calibrate, plot, and fetch parameters of equation
params = calibrate.run_calibration()

# distance_this = calibrate.inv_exponential(280 * 5 / 1023, *params)
# print(prd.angle_to_coordinates([280 * 5 / 1023], [[0], [0]], params))
# Fetch data until STOP command given
sensor_volt, positions, radii = prd.fetch_data(serial_port, get_data=True, params=params)

# Generate image of object
prd.plot_heatmap(positions, radii)