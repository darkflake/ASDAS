import matplotlib.pyplot as plt
from data_preprocessing.savitsky_golay import savitzky_golay
import numpy as np


def interpolate(raw_data: list, x_values: str, interpolation_points: list):
    interpolated_data = raw_data.copy()                                              # Retain original data:

    for x, y in list(zip(interpolation_points, interpolation_points[1:]))[::2]:      # Read interpolation points from list
        x, y = x_values.index(x), x_values.index(y)                                  # Get the number of entry on X-Axis
        slope = (raw_data[y] - raw_data[x])/(y-x)                                    # Slope of line in the two points

        for i in range(x+1, y):                                                      # Calculate Y value for every point
            interpolated_data[i] = interpolated_data[x] + (i-x)*slope                # y = mx + c

    graph(raw_data, x_values, interpolated_data)                                     # Render original + interpolated data


# Render graphs:
def graph(data_y, data_x, interpolated_data=None):
    plt.plot(data_y, '-bo', label='Actual Data')

    sav = savitzky_golay(y=np.asarray(data_y), window_size=5, order=3)
    plt.plot(sav, '--g', label='SavGol Filter')

    if interpolated_data:
        plt.plot(interpolated_data, ':ro', label='Interpolated Data')
        sav_interpolated = savitzky_golay(y=np.asarray(interpolated_data), window_size=5, order=3)
        plt.plot(sav_interpolated, '--y', label='SavGol Filter (interpolated)')

    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title('Interpolation')

    plt.xticks(range(0, len(data_y)), data_x)
    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.legend()

    plt.show()


# Play :
# basic_y = [10, 20, 40, 60, 70, 30, 20, 40, 80, 110, 160, 120, 100, 180, 200]
# basic_x = [str(d)+"/1" for d in range(1, 16)]
#
# interpolate(basic_y, basic_x, ['5/1', '11/1', '11/1', '14/1'])
