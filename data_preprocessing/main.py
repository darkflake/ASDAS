import os
import pandas as pd
import time

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
    # name_of_class = input("Select Class [Agriculture/BarrenLand/Forests/Infrastructure/Water] : ")
    # name_of_band = input("Band to plot [Blue/Green/Red/NIR/SWIR/SCL / NDVI/NDWI/NDWI] : ")
    # pixel_index = int(input("Pixel Index : "))
    name_of_class = 'Forests'
    name_of_band = 'NDVI'
    pixel_index = 0
    input_csv = pd.read_csv(
        os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{name_of_class}/{name_of_band}.csv")  # Get csv

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


def display(input_data: pd.DataFrame, name_of_band: str, pixel_index: int = 0, interpolate_points: list = None,
            apply_filter=False, do_interpolate=False):
    r"""
    Renders the graph for the given data for the given pixel index.

    :param input_data: input data
    :param pixel_index: which data point (pixel) to render : 0-699
    :param name_of_band: Red / Green / Blue / NIR / NDVI / NDWI / NDBI
    :param interpolate_points: list of points to perform interpolation between
    :param apply_filter: Apply and render Savitsky-Golay filter
    :param do_interpolate: Perform interpolation on data
    :return: None
    """
    print(
        f"Min value : {min(input_data.values.tolist()[pixel_index][2:])} , "
        f"Max value : {max(input_data.values.tolist()[pixel_index][2:])}")

    if do_interpolate:
        interpolate(input_data=input_data.values.tolist()[pixel_index][2:], display=True, apply_filter=apply_filter,
                    x_values=input_data.columns.tolist(), band=name_of_band, title=str(pixel_index),
                    interpolation_points=interpolate_points)
    else:
        graph(data_y=input_data.values.tolist()[pixel_index][2:], band=name_of_band, title=str(pixel_index),
              savgol=apply_filter)


# _____________________________________


def write_csv(input_data: pd.DataFrame, name_of_class: str, file_name: str):
    r"""
    Write the input DataFrame into CSV in Data_2019/CSV folder
    :param input_data: Input data
    :param name_of_class: Specify class of the data
    :param file_name: Name of file to be saved
    :return: None
    """
    input_data.to_csv(os.path.abspath(__file__ + "/../../") + f"/data_2019/CSV/{name_of_class}/{file_name}.csv",
                      index=False)
    print("Data Written")

# _____________________________________


def get_cloud_dates(pixel_index: int, name_of_class: str):
    input_data = pd.read_csv(
        os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{name_of_class}/SCL.csv")
    cloud_dates = []
    count = 0
    row_values = input_data.iloc[pixel_index]
    last_element = pd.Series([-1])
    row_values.append(last_element)
    column_values = input_data.columns.tolist()

    for current in range(len(row_values)):
        if row_values[current] == 8 or row_values[current] == 9 or row_values[current] == 10:
            if count == 0:
                before = current - 1
                if before in cloud_dates:
                    continue
                else:
                    cloud_dates.append(column_values[before])
            count = count + 1
        else:
            if 1 <= count <= 3:
                after = current
                cloud_dates.append(column_values[after])
            else:
                if cloud_dates:
                    if count != 0:
                        cloud_dates.pop()

        if row_values[current] != 8 and row_values[current] != 9 and row_values[current] != 10:
            count = 0

    return cloud_dates

# _____________________________________


def preprocess():
    r"""
    Perform pre-processing on data. ( Handle missing values + Cloud Correction using Interpolation + SavGol filtering )
    The function calls  get_data() -> checks for stored preprocessed data.
    If not found, performs following functions:
    -> Finding and Handling NaN values.
    -> Getting cloud dates - Atmospheric Correction.
    -> Linearly Interpolating between cloud dates.
    -> Applying Savitsky-Golay filter.

    :return: dictionary with interpolated and filtered DataFrames
    """

    class_name, band_name, pixel_index, input_data = get_data()

    preprocessed = {'original': input_data}

    try:
        working_csv = pd.read_csv(
            os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{class_name}/preprocessed_{band_name}.csv")

    except FileNotFoundError as e:
        no_nan_csv = fix_nan(input_data)
        working_csv = no_nan_csv.copy()

        for index in range(0, len(working_csv.index)):
            interpolation_points = get_cloud_dates(pixel_index=index, name_of_class=class_name)

            interpolated_csv = apply_interpolation(input_data=working_csv, index=index,
                                                   interpolation_points=interpolation_points)

            filtered_csv = apply_savgol(data_csv=interpolated_csv, index=index, window=7, order=3)

            working_csv = filtered_csv
            print(f"Done For : {index}")

        write_csv(preprocessed['preprocessed'], class_name, file_name=f"preprocessed_{band_name}")

    preprocessed['preprocessed'] = working_csv

    index_files = {}
    bands = ['NDVI', 'NDWI', 'NDBI']
    for band in bands:
        index_files[band] = pd.read_csv(
            os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{class_name}/preprocessed_{band}.csv")

    preprocessed['index files'] = index_files

    return class_name, pixel_index, band_name, preprocessed


# _____________________________________________________________________________________________________________________
# Play:
'''
name_of_class, index, name_of_band, csv_data = preprocess()

interpolating_dates = get_cloud_dates(pixel_index=index, name_of_class=name_of_class)

interpolated_data = apply_interpolation(csv_data['original'], index=index, interpolation_points=interpolating_dates)

display(input_data=csv_data['original'], pixel_index=index, name_of_band=name_of_band, do_interpolate=False,
        interpolate_points=interpolating_dates, apply_filter=False)

display(input_data=csv_data['original'], pixel_index=index, name_of_band=name_of_band, do_interpolate=True,
        interpolate_points=interpolating_dates, apply_filter=False)

display(input_data=interpolated_data, pixel_index=index, name_of_band=name_of_band, do_interpolate=False,
        interpolate_points=interpolating_dates, apply_filter=False)

display(input_data=interpolated_data, pixel_index=index, name_of_band=name_of_band, do_interpolate=False,
        interpolate_points=interpolating_dates, apply_filter=True)

display(input_data=csv_data['preprocessed'], pixel_index=index, name_of_band=name_of_band, do_interpolate=False,
        interpolate_points=interpolating_dates, apply_filter=False)


'''
'''
FOR WHOLE RAW DATA : 

def preprocess():
    start_time = time.time()
    counter = 0
    
    bands = ['NDVI', 'NDWI', 'NDBI']
    classes = ['Forests', 'Water', 'Agriculture', 'BarrenLand', 'Infrastructure']
    for label in classes:
        for band in bands:
            input_data = pd.read_csv(
                os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{label}/{band}.csv")
            no_nan_csv = fix_nan(input_data)
            working_csv = no_nan_csv.copy()
            print("__________________________________________________")
            print(f"Working : {label} - {band}")
            print("__________________________________________________")
    
            for index in range(0, len(no_nan_csv.index)):
                interpolation_points = get_cloud_dates(pixel_index=index, name_of_class=label)
    
                interpolated_csv = apply_interpolation(input_data=working_csv, index=index,
                                                       interpolation_points=interpolation_points)
    
                filtered_csv = apply_savgol(data_csv=interpolated_csv, index=index, window=7, order=3)
    
                working_csv = filtered_csv
                counter += 1
                print(f"_________________Done For : {index} ________ Total Data Points Count : {counter}")
            write_csv(filtered_csv, label, file_name=f"preprocessed_{band}")
            print(f"== Total time spend until now : == {round(time.time() - start_time)}s == ")

'''
