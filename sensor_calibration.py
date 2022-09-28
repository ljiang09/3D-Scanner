"""
Calibration for IR Sensor
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Readings taken at 4 cm intervals starting at 20 cm
DISTANCES = np.array([20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 90, 110, 120, 130, 140])
READINGS = np.array([500, 470, 410, 395, 345, 315, 286, 255, 240, 210, 195, 180, 170, 160, 120, 95, 85, 80, 75]) #300, 240, 210, 185, 170, 157, 153, 145])

# Readings taken at distances (cm) specified in 
TEST_DATA = np.array([[30, 38, 43, 53, 66, 73], [400, 330, 298, 230, 180, 160]])

def exponential(x, a, b, c):
    """
    Distance to Voltage
    TODO:
    """
    return (a * np.exp((b * x))) + c

def inv_exponential(v, a, b, c):
    """
    Voltage to Distance
    TODO:
    """
    return (np.log((v - c)/a)/b)

def generate_calibration_plot(distances_cm, readings):
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
    # distances_cm = 2.54 * distances
    readings_volt = readings * 5 / 1023

    # Plot reading against 1/distance
    plt.plot(distances_cm, readings_volt, 'ro', label="Collected Data")
    plt.xlabel("Distance (cm)")
    plt.ylabel("IR Sensor Reading (V)")
    plt.title("IR Sensor Readings over Distance")

    # Fit line
    param, cov = curve_fit(f=exponential, xdata=distances_cm, ydata=readings_volt,
        bounds=(-np.inf, np.inf), p0=[850.0, -0.01, -50.0])
    print(f"Curve Fit Equation: {param[0]} * e ^ {param[1]}x + {param[2]}")

    # Plot fitted line
    plt.plot(distances_cm, exponential(distances_cm, *param), 'b', label="Fitted Line")
    plt.legend()
    plt.show()

    return param

def test_calibration_curve(distances_cm, param, test_data):
    """
    TODO: 
    """
    readings_volt = test_data[1] * 5 / 1023

    plt.clf
    plt.plot(test_data[0], exponential(test_data[0], *param), 'ro', label="Predicted Data")
    plt.plot(test_data[0], readings_volt, 'bo', label="Collected Data")
    plt.xlabel("Distance (cm)")
    plt.ylabel("IR Sensor Reading (V)")
    plt.legend()
    plt.title("Actual vs Predicted IR Sensor Readings")
    plt.show()

def run_calibration():
    """
    TODO:
    """
    params = generate_calibration_plot(DISTANCES, READINGS)
    test_calibration_curve(DISTANCES, params, TEST_DATA)
    return params


