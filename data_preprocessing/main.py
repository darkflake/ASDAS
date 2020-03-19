import os
import pandas as pd
import numpy as np

from data_preprocessing.interpolation import interpolate, graph, apply_interpolation
from data_preprocessing.savitsky_golay import apply_savgol


def write_csv(input_data: pd.DataFrame, name_of_class: str, file_name: str):
    r"""
    Write the input DataFrame into CSV in Data_2019/CSV folder
    :param input_data: Input data
    :param name_of_class: Specify class of the data
    :param file_name: Name of file to be saved
    :return: None
    """
    input_data.to_csv(os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{name_of_class}/{file_name}.csv", index=False)
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


def get_data():
    name_of_class = input("Select Class [Forests/Water] : ")
    name_of_band = input("Band to plot [Blue/Green/Red/NIR/SWIR/SCL / NDVI] : ")
    pixel_index = int(input("Pixel Index : "))
    # name_of_band = 'NDVI'
    # pixel_index = 0

    input_csv = pd.read_csv(os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{name_of_class}/{name_of_band}.csv")  # Get csv
    return name_of_class, name_of_band, pixel_index, input_csv
# _____________________________________


def display(input_csv: pd.DataFrame, name_of_band: str, pixel_index: int = 0, interpolate_points: list = None,
            apply_filter=False, do_interpolate=False):
    r"""
    Renders the graph for the given data for the given pixel index.

    :param input_csv: input data
    :param pixel_index: which data point (pixel) to render : 0-27
    :param name_of_band: Red / Green / Blue / NIR / NDVI
    :param interpolate_points: list of points to perform interpolation between
    :param apply_filter: Apply and render Savitsky-Golay filter
    :param do_interpolate: Perform interpolation on data
    :return: None
    """
    print(f"Min value : {min(input_csv.values.tolist()[index][2:])} , Max value : {max(input_csv.values.tolist()[index][2:])}")

    if do_interpolate:
        interpolate(raw_data=input_csv.values.tolist()[pixel_index][2:], display=True, apply_filter=apply_filter,
                    x_values=input_csv.columns.tolist(), band=name_of_band, title=str(pixel_index),
                    interpolation_points=interpolate_points)
    else:
        graph(data_y=input_csv.values.tolist()[pixel_index][2:], band=name_of_band, title=str(pixel_index), savgol=apply_filter)
# _____________________________________


def perform(input_csv: pd.DataFrame):
    r"""
    Perform pre-processing on data. ( Handle missing values + Cloud Correction using Interpolation + SavGol filtering )
    :param input_csv: raw data
    :return: dictionary with interpolated and filtered DataFrames
    """
    no_nan_csv = fix_nan(csv)

    interpolated_csv = apply_interpolation(data_csv=no_nan_csv, index=index, interpolation_points=interpolation_points)

    filtered_csv = apply_savgol(data_csv=interpolated_csv, index=index, window=7, order=3)

    processed = {'Interpolated': interpolated_csv, 'Filtered': filtered_csv}
    return processed


# Play:
interpolation_points = ['2019-06-04', '2019-07-19', '2019-07-19', '2019-08-23', '2019-08-23', '2019-09-22',
                        '2019-09-22', '2019-10-02', '2019-10-17', '2019-11-06', '2019-12-11', '2019-12-31']

class_name, band_name, index, csv = get_data()
print("___")

interpolated_data, filtered_data = perform(csv)


# write_csv(filtered_csv, class_name, f"filtered-{band_name}")

display(input_csv=csv, pixel_index=index, name_of_band=band_name, do_interpolate=False, apply_filter=True,
        interpolate_points=interpolation_points)

# _____________________________________________________________________________________________________________________
# print(no_nan_csv.columns.tolist())                   Get list of columns

# columns = no_nan_csv.columns.tolist()[2:]           Get entry for every new month for X-Axis labels
# for entry in columns:
#     month = entry[5:7]
#     print(month)
#     if month == init_month:
#         continue
#     else:
#         labels.append(entry)
#         indexes.append(columns.index(entry))
#         init_month = month
