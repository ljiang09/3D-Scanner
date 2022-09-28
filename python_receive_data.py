"""
Listens for data from the Arduino scanner, generates a 3D visualization of
the scanned object.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
import csv

import sensor_calibration as calibrate

def fetch_data(serial_port, get_data, params):
  """
  Listens for and gathers data from the Arduino scanner.
  Args:
    serial_port: A serial port object representing the port associated with
        the Arduino.
    get_data: A bool representing whether data from the Arduino should be
        gathered at the moment.
    params: A float array representing the coefficients and transformations
        that define the sensor's calibration curve.
  Returns:
    sensor_volt: The voltages read in by the IR sensor.
    positions: A 3 row array representing the x, y, and z values (respectively)
        calculated for each of the values the sensor reads in.
    radii: The distances measured by the IR sensor (calculated using the
        calibration curve).
  """
  sensor_volt = []
  position_degrees = [[], []]

  # open a csv file to write into
  f = open("recording_data2.csv", "w")
  writer = csv.writer(f)
  writer.writerow(["value", "pan_degree", "tilt_degree"])

  # Fetch data from Arduino
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
  Converts pan/tilt angles to Cartesian coordinates.
  Notes: 
    Z is plane that the servo is on (Z-distance is distance between servo and
        the letter).
    Center at 90 degrees for x sweep servo and 90 for y sweep servo.
  Args:
    sensor_volt: The voltages read in by the IR sensor.
    position_degrees: A 2-row array representing the pan and tilt angles
        (respectively).
    params: A float array representing the coefficients and transformations
        that define the sensor's calibration curve.
  Returns:
    np.array(positions): A 3-row array representing the x, y, and z values
        (respectively) calculated for each of the values the sensor reads in.
    radii: The distances measured by the IR sensor (calculated using the
        calibration curve).
  """
  pan_degrees = np.array(position_degrees[0])
  tilt_degrees = np.array(position_degrees[1])

  # Convert sensor data to distances
  radii = calibrate.inv_exponential(sensor_volt, *params)

  # Center the angles so that 90 degrees is 0 (At '90 degrees', new 0, distance = radius) for x + y
  pan_degrees -= 30 # phi
  tilt_degrees -= 10 # theta

  positions = [[], [], []]

  f = open("n_data2.csv", 'w')
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

    # print(f"X: {x}")
    # print(f"Y: {y}")
    # print(f"Z: {z}")

    writer.writerow([x, y, z, radii[index]])

  f.close()
  positions = filter_data(positions)
  return np.array(positions), radii

def read_position_from_csv(filepath):
  """
  TODO:
  """
  positions = [[], [], []]

  with open('n_data2.csv', 'r') as f:
    file = csv.reader(f)
    next(file)
    for row in file:
      positions[0].append(float(row[0]))
      positions[1].append(float(row[1]))
      positions[2].append(float(row[2]))
  
  return positions

def filter_data(positions):
  """
  TODO:
  """
  x = positions[0]
  y = positions[1]
  z = positions[2]

  new_positions = [[], [], []]
  for point in range(len(y)):
    if float(y[point]) < 60:
        new_positions[0].append(float(x[point]))
        new_positions[1].append(float(y[point]))
        new_positions[2].append(float(z[point]))
  
  return new_positions

def plot_heatmap(positions):
  """
  Plots the scanned datapoints in the Cartesian system.
  Args:
    positions: A 3 row array representing the x, y, and z values (respectively)
        calculated for each of the values the sensor reads in.
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
  
