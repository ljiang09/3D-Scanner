"""
TODO:
"""
import numpy as np
import matplotlib.pyplot as plt

import sensor_calibration as calibrate

def fetch_data(serial_port, get_data):
  """
  TODO: 
  """
  sensor_volt = []
  position_degrees = [[], []]

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

  return (sensor_volt, position_degrees)

def plot_heatmap(sensor_volt, params):
  """
  TODO:
  """
  # Data to distances
  distances = calibrate.exponential(sensor_volt, *params)

  # Plot data
  plt.clf
  plt.imshow(distances, cmap="PiYG")
  plt.colorbar()
  plt.show()
  plt.title("Heatmap of Distances")
  
