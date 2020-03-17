import matplotlib.pyplot as plt
from data_preprocessing.savitsky_golay import savitzky_golay
import numpy as np
import pandas as pd


def interpolate(raw_data: list, x_values: str, interpolation_points: list, title: str = None, band: str = None, display=False, apply_filter=False):
    interpolated_data = raw_data.copy()                                                                                 # Retain original data

    for x, y in list(zip(interpolation_points, interpolation_points[1:]))[::2]:                                         # Read interpolation points
        x, y = x_values.index(x)-2, x_values.index(y)-2
        slope = (raw_data[y] - raw_data[x])/(y-x)                                                                       # Slope of line in the two points

        for i in range(x+1, y):                                                                                         # Calculate Y value for every point
            interpolated_data[i] = interpolated_data[x] + (i-x)*slope                                                   # y = mx + c

    if display:
        graph(raw_data, band=band, title=title, interpolated_data=interpolated_data, savgol=apply_filter)               # Render graphs

    return interpolated_data


def apply_interpolation(data_csv: pd.DataFrame, index: int, interpolation_points: list):
    r"""
            Apply Linear Interpolation to every row of the data frame.

    :param data_csv: input data
    :param index: index of row to interpolate on
    :param interpolation_points: list of points to interpolate between
    :return: None
    """
    copy_data_csv = data_csv.copy()
    old_row = data_csv.values.tolist()[index][2:]
    new_row = data_csv.values.tolist()[index][:2]

    inter = interpolate(raw_data=old_row, x_values=data_csv.columns.tolist(), interpolation_points=interpolation_points)
    new_row.extend([x for x in inter])

    copy_data_csv.loc[index] = new_row

    print("Applied Interpolation.")
    # graph(data_y=data_csv.values.tolist()[index][2:])
    return copy_data_csv


# Render graphs:
def graph(data_y, title='Data', band="", interpolated_data=None, savgol=False):
    labels = ['05 Jan', '04 Feb', '01 Mar', '05 Apr', '05 May', '04 Jun', '04 Jul', '03 Aug', '02 Sep', '02 Oct',
              '01 Nov', '01 Dec']
    indexes = [0, 6, 11, 18, 24, 30, 36, 42, 48, 54, 60, 66]

    plt.plot(data_y, '-go', label='Actual Data', alpha=0.3)

    if interpolated_data:
        plt.plot(interpolated_data, ':r', label='Interpolated Data', alpha=0.5)
        if savgol:
            sav = savitzky_golay(y=np.asarray(interpolated_data), window_size=7, order=3)

    else:
        if savgol:
            sav = savitzky_golay(y=np.asarray(data_y), window_size=7, order=3)

    if savgol:
        plt.plot(sav, '--b', label='SavGol Filter', alpha=1)

    plt.xlabel('2019')
    plt.ylabel(f'Band Value ({band})')
    plt.title(f"Pixel: {title}")
    plt.ylim([-0.3, 1])

    plt.xticks(indexes, labels, rotation=20)
    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.legend()

    plt.show()
    # plt.savefig(f'{title}.png')
    # plt.close()


# Play :
# basic_y = [10, 20, 40, 60, 70, 30, 20, 40, 80, 110, 160, 120, 100, 180, 200]
# basic_x = [str(d)+"/1" for d in range(1, 16)]
#
# interpolate(basic_y, basic_x, ['5/1', '11/1', '11/1', '14/1'])
