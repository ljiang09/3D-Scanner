"""
Calibration for IR Sensor
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Readings taken at 4 cm intervals starting at 20 cm
DISTANCES = np.array(
    [20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 90, 110, 120, 130, 140])
READINGS = np.array(
    [500, 470, 410, 395, 345, 315, 286, 255, 240, 210, 195, 180, 170, 160, 120, 95, 85, 80, 75])

# Readings taken at distances (cm) specified in 
TEST_DATA = np.array([[30, 38, 43, 53, 66, 73], [400, 330, 298, 230, 180, 160]])

def exponential(x, a, b, c):
    """
    Convert distances in centimeters to voltage values

    Equation: v = ae^(bx) + c

    Args:
        x: A float representing the distance in centimeters from the scanner
        a: A float representing the parameter 'a' in the equation above
        b: A float representing the parameter 'b' in the equation above
        c: A float representing the parameter 'c' in the equation above
    
    Returns:
        A float representing the resulting voltage from the equation with inputs entered
    """
    return (a * np.exp((b * x))) + c

def inv_exponential(v, a, b, c):
    """
    Convert voltages to distances in centimeters

    Equation: x = ln((v - c)/a) / b

    Args:
        v: A float representing the voltage value from the scanner's measured value
        a: A float representing the parameter 'a' in the equation above
        b: A float representing the parameter 'b' in the equation above
        c: A float representing the parameter 'c' in the equation above

    Returns: 
        A float representing the resulting distance in centimeters from the voltage
    """
    return (np.log((v - c)/a)/b)

def generate_calibration_plot(distances_cm, readings):
    """
    Based on data generated from an IR sensor located at different distances from a wall, a
    calibration plot is created

    Args:
        distances_cm: An numpy array representing the distances from where readings were taken in
            centimeters
        readings: A numpy array representing the readings from the arduino (0 to 5V mapped to
            integers 0 to 1023)
    Return:
        param: A list of parameters (a, b, c) for the exponential and inv_exponential functions
            above fitted to the data entered.
    """
    # Convert reading to correct units (V)
    readings_volt = readings * 5 / 1023

    # Plot reading against distance
    plt.plot(distances_cm, readings_volt, 'ro', label="Collected Data")
    plt.xlabel("Distance (cm)")
    plt.ylabel("IR Sensor Reading (V)")
    plt.title("IR Sensor Readings over Distance")

    # Fit curve
    param, cov = curve_fit(f=exponential, xdata=distances_cm, ydata=readings_volt,
        bounds=(-np.inf, np.inf), p0=[850.0, -0.01, -50.0])
    print(f"Curve Fit Equation: {param[0]} * e ^ {param[1]}x + {param[2]}")

    # Plot fitted curve
    plt.plot(distances_cm, exponential(distances_cm, *param), 'b', label="Fitted Line")
    plt.legend()
    plt.show()

    return param

def test_calibration_curve(param, test_data):
    """
    Test the calibration curve generated through generate_calibration_plot with test data. Find
    voltages for known distances and compare those values to calculated distances. This is depicted
    through a plot

    Args:
        param: A list of parameters (a, b, c) for the exponential and inv_exponential functions
            above fitted to the data entered.
        test_data: A np.array of data with the first row having actual distances in centimeters and
            recorded values from the sensor (NOT volts) in the second row
    """
    readings_volt = test_data[1] * 5 / 1023

    plt.clf
    plt.plot(inv_exponential(readings_volt, *param), readings_volt, 'ro', label="Predicted Data")
    plt.plot(test_data[0], readings_volt, 'bo', label="Collected Data")
    plt.xlabel("Distance (cm)")
    plt.ylabel("IR Sensor Reading (V)")
    plt.legend()
    plt.title("Actual vs Predicted IR Sensor Readings")
    plt.show()

def run_calibration():
    """
    Runner function for calibration. This generates a calibration plot and uses the parameters
    to test distances. The parameters are also returned for further usage.

    Returns:
        params: A list of parameters (a, b, c) for the exponential and inv_exponential functions
            above fitted to the data entered.
    """
    params = generate_calibration_plot(DISTANCES, READINGS)
    test_calibration_curve(params, TEST_DATA)
    return params
