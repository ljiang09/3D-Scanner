"""
TODO:
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import csv

import sensor_calibration as calibrate

def fetch_data(serial_port, get_data, params):
  """
  TODO: 
  """
  sensor_volt = []
  position_degrees = [[], []]

  # Fetch data
  while get_data:
    data_line = serial_port.readline()

    try:
      data_line = data_line.decode("utf-8")
      # End fetching if "STOP" is read in from Arduino code
      if data_line == "STOP\r\n":
        get_data = False

      # Convert reading to voltage
      if len(data_line) > 4:
        data_split = data_line.split(',')

        if len(data_split) == 3:
          try:
            sensor_volt.append(float(data_split[0]) * 5 / 1023)    
            position_degrees[0].append(float(data_split[1]))
            position_degrees[1].append(float(data_split[2]))
          except:
            print("Got empty result")

        print(data_split)

    except:
      print("Couldn't decode the line")

  sensor_volt = np.array(sensor_volt)
  positions, radii = angle_to_coordinates(sensor_volt, position_degrees, params)
  return (sensor_volt, positions, radii)

def angle_to_coordinates(sensor_volt, position_degrees, params):
  """
  TODO:
  **Z is plane that the servo is on (Z-distance is distance between servo and letter)
  Center at 90 degrees for x sweep servo and 90 for y sweep servo
  """
  pan_degrees = np.array(position_degrees[0])
  tilt_degrees = np.array(position_degrees[1])

  # Data to distances
  radii = calibrate.inv_exponential(sensor_volt, *params)
  print(sensor_volt, radii)

  # Center the angles so that 90 degrees is 0 (At '90 degrees', new 0, distance = radius) for x + y
  pan_degrees -= 30 # phi
  tilt_degrees -= 10 # theta

  positions = [[], [], []]

  f = open("n_data.csv", 'w')
  writer = csv.writer(f)
  writer.writerow(["x", "y", "z", "radii"])

  for index in range(len(pan_degrees)):

    # Convert degrees to radians
    pan_radian = np.radians(pan_degrees[index])
    tilt_radian = np.radians(tilt_degrees[index])

    x = radii[index] * np.cos(tilt_radian) * np.sin(pan_radian)
    y = radii[index] * np.sin(tilt_radian)
    z = radii[index] * np.cos(tilt_radian) * np.cos(pan_radian)

    # Convert spherical to cartesian
    # y = radii[index] * np.sin(tilt_radian)
    # x = radii[index] * np.cos(tilt_radian) * np.cos(pan_radian)
    # z = radii[index] * np.cos(tilt_radian) * np.sin(pan_radian)

    # y = radii[index] * np.sin(tilt_radian)
    # x = radii[index] * np.sin(pan_radian)
    # z = radii[index] * np.cos(tilt_radian) * np.cos(pan_radian)

    positions[0].append(x)
    positions[1].append(y)
    positions[2].append(z)

    writer.writerow([positions[0], positions[1], positions[2], radii[index]])

  f.close()

  return np.array(positions), radii

def plot_heatmap(positions, radii):
  """
  TODO:
  """
  fig = plt.figure()
  ax = plt.axes(projection ='3d')
  # ax.scatter(positions[0], positions[1], positions[2], 'green')
  ax.scatter(positions[0], positions[1], positions[2])
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  plt.show()
  plt.title("Heatmap of Distances")
  
