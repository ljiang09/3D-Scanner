"""
TODO:
"""
from argparse import RawDescriptionHelpFormatter
import numpy as np
import matplotlib.pyplot as plt

import sensor_calibration as calibrate

def fetch_data(serial_port, get_data, z_distance, params):
  """
  TODO: 
  """
  sensor_volt = []
  position_degrees = [[], []]
  sweep_params = [[0, 180], [0, 180]]

  # Fetch data
  while get_data:
    data_line = serial_port.readline().decode()

    # End fetching if "STOP" is read in from Arduino code
    if data_line is "STOP":
      get_data = False

    # Convert reading to voltage
    if len(data_line) > 0:
      data_split = data_line.split(',')
      position_degrees[0].append(float(data_split[1]))
      position_degrees[1].append(float(data_split[2]))
      sensor_volt.append(float(data_split[0]) * 5 / 1023)

  positions = angle_to_coordinates(position_degrees, z_distance, params)
  return (sensor_volt, positions)

def angle_to_coordinates(sensor_volt, position_degrees, params):
  """
  TODO:
  **Z is plane that the servo is on (Z-distance is distance between servo and letter)
  Center at 90 degrees for x sweep servo and 90 for y sweep servo
  """
  pan_degrees = np.array(position_degrees[0])
  tilt_degrees = np.array(position_degrees[1])

  # Data to distances
  radii = calibrate.exponential(sensor_volt, *params)

  # Center the angles so that 90 degrees is 0 (At '90 degrees', new 0, distance = radius) for x + y
  x_degrees -= 90
  y_degrees -= 90

  positions = [[], [], []]

  for index in len(x_degrees):

    # Convert degrees to radians
    pan_radian = np.radians(x_degrees[index])
    tilt_radian = np.radians(y_degrees[index])

    # Convert spherical to cartesian
    y = radii[index] * np.sin(tilt_radian)
    x = radii[index] * np.cos(tilt_radian) * np.cos(pan_radian)
    z = radii[index] * np.cos(tilt_radian) * np.sin(pan_radian)

    positions[0].append(x)
    positions[1].append(y)
    positions[2].append(z)
  
  return np.array(positions)

def plot_heatmap(positions):
  """
  TODO:
  """
  plt.clf 
  plt.scatter(positions[0], positions[1], positions[2])
  plt.show()
  plt.title("Heatmap of Distances")
  
