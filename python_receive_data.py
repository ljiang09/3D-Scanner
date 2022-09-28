"""
TODO:
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
import csv

import sensor_calibration as calibrate

def fetch_data(serial_port, get_data, params):
  """
  TODO: 
  """
  sensor_volt = []
  position_degrees = [[], []]

  f = open("recording_data1.csv", "w")
  writer = csv.writer(f)
  writer.writerow(["value", "pan_degree", "tilt_degree"])

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
            position_degrees[0].append(float(data_split[1])) # Pan
            position_degrees[1].append(float(data_split[2])) # Tilt
          except:
            print("Got empty result")

        print(data_split)
        writer.writerow([float(data_split[0]), float(data_split[1]), float(data_split[2])])

    except:
      print("Couldn't decode the line")

  f.close()

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

  # # Center the angles so that 90 degrees is 0 (At '90 degrees', new 0, distance = radius) for x + y
  # pan_degrees -= 30 # phi
  # tilt_degrees -= 10 # theta

  positions = [[], [], []]

  f = open("n_data1.csv", 'w')
  writer = csv.writer(f)
  writer.writerow(["x", "y", "z", "radii"])

  for index in range(len(pan_degrees)):
    # Convert degrees to radians
    pan_radian = np.radians(pan_degrees[index])
    tilt_radian = np.radians(tilt_degrees[index])

    x = radii[index] * np.sin((np.pi / 2) - tilt_radian) * np.cos((np.pi / 2) - pan_radian)
    y = radii[index] * np.sin((np.pi / 2) - tilt_radian) * np.sin((np.pi / 2) - pan_radian)
    z = radii[index] * np.cos((np.pi / 2) - tilt_radian)

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

    writer.writerow([x, y, z, radii[index]])

  f.close()
  positions = filter_data(positions)
  return np.array(positions), radii

def filter_data(positions):
  """
  TODO:
  """
  x = positions[0]
  y = positions[1]
  z = positions[2]

  

def plot_heatmap(positions, radii):
  """
  TODO:
  """
  fig = plt.figure()
  ax = plt.axes(projection ='3d')
  # ax.scatter(positions[0], positions[1], positions[2], 'green')
  ax.scatter3D(positions[0], positions[1], positions[2])
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  ax.set_zlabel("Z")
  plt.show()
  plt.title("Heatmap of Distances")
  
