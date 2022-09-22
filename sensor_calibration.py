"""
Calibration for IR Sensor
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Readings taken at 4 inch intervals starting at 8 inches
DISTANCES = np.array(range(8, 45, 4))
READINGS = np.array([490, 385, 300, 240, 210, 185, 170, 157, 153, 145])

TEST_DATA = np.array([[30, 40, 27, 66.04, 53.34, 73.66], [390, 307, 415, 196, 240, 193]])
print(TEST_DATA[0])

def exponential(x, a, b, c):
    """
    """
    return (a * np.exp((b * x))) + c

def generate_calibration_plot(distances, readings):
    """
    Based on data generated from an IR sensor located at different distances from a wall, a
    calibration plot is created

    Args:
        distances: An numpy array representing the distances from where readings were taken in
            inches
        readings: A numpy array representing the readings from the arduino (0 to 5V mapped to
            integers 0 to 1023)

    Return:
        params: TODO: WRITE THIS IN
    """
    # Convert to correct units
    distances_cm = 2.54 * distances
    readings_volt = readings * 5 / 1023

    # Plot reading against 1/distance
    plt.plot(distances_cm, readings_volt, 'o', label="Collected Data")
    plt.xlabel("Distance (cm)")
    plt.ylabel("IR Sensor Reading (V)")
    plt.title("IR Sensor Readings over Distance")

    # Fit line
    param, cov = curve_fit(f=exponential, xdata=distances_cm, ydata=readings_volt,
        bounds=(-np.inf, np.inf), p0=[750.0, -0.1, 100.0])
    print(f"Curve Fit Equation: {param[0]} * e ^ {param[1]}x + {param[2]}")

    # Plot fitted line
    plt.plot(distances_cm, exponential(distances_cm, *param), 'g', label="Fitted Line")
    plt.legend()
    plt.show()

    return param

def test_calibration_curve(distances_cm, param, test_data):
    """
    """
    readings_volt = test_data[1] * 5 / 1023

    plt.clf
    plt.plot(test_data[0], exponential(test_data[0], *param), 'o')
    plt.plot(test_data[0], readings_volt, 'go')
    plt.show()


param = generate_calibration_plot(DISTANCES, READINGS)
test_calibration_curve(DISTANCES * 2.54, param, TEST_DATA)
