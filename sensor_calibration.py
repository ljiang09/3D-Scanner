"""
Calibration for IR Sensor
"""

import numpy as np
import matplotlib.pyplot as plt

# Readings taken at 4 inch intervals starting at 8 inches
DISTANCES = np.array(range(8, 45, 4))
READINGS = np.array([490, 385, 300, 240, 210, 185, 170, 157, 153, 145])


def generate_calibration_plot(distances, readings):
    """
    Based on data generated from an IR sensor located at different distances from a wall, a
    calibration plot is created

    Args:
        distances: An numpy array representing the distances from where readings were taken in
            inches
        readings: A numpy array representing the readings from the arduino (0 to 5V mapped to
            integers0 to 1023)

    Returns:

    """
    # Convert to correct units
    distances_cm = 2.54 * distances
    readings_volt = readings * 5 / 1023

    inv_distances_cm = np.ones(len(readings_volt))/distances_cm

    # Plot reading against 1/distance
    plt.plot(inv_distances_cm, readings_volt, 'o')
    plt.xlabel("Distance (cm)")
    plt.ylabel("IR Sensor Reading (V)")
    plt.title("IR Sensor Readings over Distance")

    # Fit line
    coeff = np.polyfit(inv_distances_cm, readings_volt, 1)
    x_fit = np.array(np.linspace(min(inv_distances_cm), max(inv_distances_cm), 1000))
    y_fit = coeff[1] + (coeff[0] * x_fit)

    # Plot fitted line
    plt.plot(x_fit, y_fit)
    plt.legend("Collected Data", "Fitted Line")
    plt.show()

generate_calibration_plot(DISTANCES, READINGS)
