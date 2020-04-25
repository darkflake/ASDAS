import matplotlib.pyplot as plt
from data_preprocessing.savitsky_golay import savitzky_golay
import numpy as np
import pandas as pd


def interpolate(input_data: list, x_values: str, interpolation_points: list, title: str = None, band: str = None, display=False, apply_filter=False):
    r"""
    Perform linear interpolation on selected points.

    :param input_data: Raw data
    :param x_values: List of x - coordinates
    :param interpolation_points: List of values which will contain points for interpolation in pairs
    :param title: Title of graph (if displayed)
    :param band: Red / Green / Blue / NIR / SWIR / NDVI
    :param display: Render graph with interpolation
    :param apply_filter: Apply Savitsky-Golay filter
    :return: DataFrame with interpolated values
    """
    interpolated_data = input_data.copy()                                                                                 # Retain original data

    for x, y in list(zip(interpolation_points, interpolation_points[1:]))[::2]:                                         # Read interpolation points
        x, y = x_values.index(x)-2, x_values.index(y)-2
        slope = (input_data[y] - input_data[x])/(y-x)                                                                       # Slope of line in the two points

        for i in range(x+1, y):                                                                                         # Calculate Y value for every point
            interpolated_data[i] = interpolated_data[x] + (i-x)*slope                                                   # y = mx + c

    if display:
        graph(input_data, band=band, title=title, interpolated_data=interpolated_data, savgol=apply_filter)               # Render graphs

    return interpolated_data


def apply_interpolation(input_data: pd.DataFrame, index: int, interpolation_points: list):
    r"""
    Apply Linear Interpolation to every row of the data frame.

    :param input_data: input data
    :param index: index of row to interpolate on
    :param interpolation_points: list of points to interpolate between
    :return: None
    """
    copy_input_data = input_data.copy()
    old_row = input_data.values.tolist()[index][2:]
    new_row = input_data.values.tolist()[index][:2]

    inter = interpolate(input_data=old_row, x_values=input_data.columns.tolist(), interpolation_points=interpolation_points)
    new_row.extend([x for x in inter])

    copy_input_data.loc[index] = new_row

    return copy_input_data


def graph(data_y, title='Data', band="", interpolated_data=None, savgol=False):
    r"""
    Render graph of values against 5-day interval of 2019 from 1 Jan to 31 Dec

    :param data_y: Data holding values
    :param title: Pixel index selected
    :param band: ed / Green / Blue / NIR / SWIR / NDVI
    :param interpolated_data: Render interpolated data
    :param savgol: Apply Savitsky-Golay filter
    :return: None
    """
    labels = ['05 Jan', '04 Feb', '01 Mar', '05 Apr', '05 May', '04 Jun', '04 Jul', '03 Aug', '02 Sep', '02 Oct',
              '01 Nov', '01 Dec']
    indexes = [0, 6, 11, 18, 24, 30, 36, 42, 48, 54, 60, 66]

    if savgol:
        savgol_alpha = 1
        curve_alpha = 0.4
    else:
        curve_alpha = 1

    plt.plot(data_y, '-go', label='Actual Data', alpha=curve_alpha)

    if interpolated_data:
        plt.plot(interpolated_data, ':r', label='Interpolated Data', alpha=curve_alpha)
        if savgol:
            sav = savitzky_golay(y=np.asarray(interpolated_data), window_size=7, order=3)

    else:
        if savgol:
            sav = savitzky_golay(y=np.asarray(data_y), window_size=7, order=3)

    if savgol:
        plt.plot(sav, '--b', label='SavGol Filter', alpha=savgol_alpha)

    plt.xlabel('2019')
    plt.ylabel(f'Band Value ({band})')
    plt.title(f"Pixel: {title}")

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
