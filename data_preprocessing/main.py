import os
import pandas as pd

from data_preprocessing.interpolation import interpolate, graph, apply_interpolation
from data_preprocessing.savitsky_golay import apply_savgol


def get_months(input_data: pd.DataFrame):
    r"""
    Get the first capture date of every month and its index in year-long csv.
    :param input_data: raw data
    :return: Tuple of labels, Indexes
    """
    columns = input_data.columns.tolist()[2:]
    labels = []
    indexes = []
    init_month = 00
    for entry in columns:
        month = entry[5:7]
        print(month)
        if month == init_month:
            continue
        else:
            labels.append(entry)
            indexes.append(columns.index(entry))
            init_month = month

    return labels, indexes
# _____________________________________


def get_data():
    name_of_class = input("Select Class [Forests/Water] : ")
    name_of_band = input("Band to plot [Blue/Green/Red/NIR/SWIR/SCL / NDVI] : ")
    pixel_index = int(input("Pixel Index : "))
    # name_of_class = 'Forests'
    # name_of_band = 'NDVI'
    # pixel_index = 0

    input_csv = pd.read_csv(os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{name_of_class}/{name_of_band}.csv")  # Get csv

    return name_of_class, name_of_band, pixel_index, input_csv
# _____________________________________


def fix_nan(input_data: pd.DataFrame):
    r"""
    Find all NaN values in the input DataFrame (if any), perform Linear Interpolation for handling missing values.

    :param input_data: input data for processing
    :return: output data without any missing values
    """
    total_nan = input_data.isna().sum().sum()  # Check if there are NaN
    print(f"Total NaN values : {total_nan}")

    if total_nan > 0:
        processed = input_data.interpolate(method='linear', axis=1, inplace=False,
                                           limit_direction='both')  # Interpolate
        print("Handled missing values")
        return processed
    else:
        return input_data
# _____________________________________


def perform(input_data: pd.DataFrame, band_index: int, interpolation_points: list):
    r"""
    Perform pre-processing on data. ( Handle missing values + Cloud Correction using Interpolation + SavGol filtering )

    :param input_data: raw data
    :param band_index: which data point (pixel) to render : 0-699
    :param interpolation_points: list of points to perform interpolation between
    :return: dictionary with interpolated and filtered DataFrames
    """
    no_nan_csv = fix_nan(input_data)

    interpolated_csv = apply_interpolation(data_csv=no_nan_csv, index=band_index, interpolation_points=interpolation_points)

    filtered_csv = apply_savgol(data_csv=interpolated_csv, index=band_index, window=7, order=3)

    processed = {'Interpolated': interpolated_csv, 'Filtered': filtered_csv}
    return processed
# _____________________________________


def display(input_data: pd.DataFrame, name_of_band: str, pixel_index: int = 0, interpolate_points: list = None,
            apply_filter=False, do_interpolate=False):
    r"""
    Renders the graph for the given data for the given pixel index.

    :param input_data: input data
    :param pixel_index: which data point (pixel) to render : 0-699
    :param name_of_band: Red / Green / Blue / NIR / NDVI
    :param interpolate_points: list of points to perform interpolation between
    :param apply_filter: Apply and render Savitsky-Golay filter
    :param do_interpolate: Perform interpolation on data
    :return: None
    """
    print(f"Min value : {min(input_data.values.tolist()[pixel_index][2:])} , Max value : {max(input_data.values.tolist()[pixel_index][2:])}")

    if do_interpolate:
        interpolate(raw_data=input_data.values.tolist()[pixel_index][2:], display=True, apply_filter=apply_filter,
                    x_values=input_data.columns.tolist(), band=name_of_band, title=str(pixel_index),
                    interpolation_points=interpolate_points)
    else:
        graph(data_y=input_data.values.tolist()[pixel_index][2:], band=name_of_band, title=str(pixel_index), savgol=apply_filter)
# _____________________________________


def write_csv(input_data: pd.DataFrame, name_of_class: str, file_name: str):
    r"""
    Write the input DataFrame into CSV in Data_2019/CSV folder
    :param input_data: Input data
    :param name_of_class: Specify class of the data
    :param file_name: Name of file to be saved
    :return: None
    """
    input_data.to_csv(os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{name_of_class}/{file_name}.csv", index=False)

# _____________________________________________________________________________________________________________________
# Play:
# interpolation_points = ['2019-06-04', '2019-07-19', '2019-07-19', '2019-08-23', '2019-08-23', '2019-09-22',
#                         '2019-09-22', '2019-10-02', '2019-10-17', '2019-11-06', '2019-12-11', '2019-12-31']
#
# class_name, band_name, index, csv = get_data()
#
# interpolated_data, filtered_data = perform(csv)
#
# display(input_data=csv, pixel_index=index, name_of_band=band_name, do_interpolate=False, apply_filter=False,
#         interpolate_points=interpolation_points)

# _____________________________________________________________________________________________________________________
# print(no_nan_csv.columns.tolist())                   Get list of columns

