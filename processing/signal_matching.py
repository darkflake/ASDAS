import pickle
import os
import time

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tslearn.metrics import dtw_path
from tslearn.barycenters import dtw_barycenter_averaging

from data_preprocessing import main
from processing import patternizer


def nd_array_to_list(input_data: np.ndarray):
    r"""
    Convert a 2D numpy.ndarray (1 x n) into a flat list.

    :param input_data: np.ndarray to flatten
    :return: flattened 1D list
    """
    return [x[0] for x in input_data.tolist()]


# _____________________________________


def get_average_curve(input_data: pd.DataFrame):
    r"""
    Find the generalized curve to represent the sample using DTW-Barycenter Averaging. (The average curve does not
    contain the geo-referencing data.)

    :param input_data: raw class data
    :return: data points for generalized curve

    """
    if 'Long' in input_data.columns:
        starting_index = 2
    else:
        starting_index = 0

    columns = input_data.columns
    general = []

    for i in range(0, len(input_data)):
        general.append(list(input_data.values.tolist()[i][starting_index:]))

    generalized = dtw_barycenter_averaging(general,
                                           metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
                                           max_iter=3)

    generalized = nd_array_to_list(generalized)

    return pd.DataFrame([generalized], columns=columns[starting_index:])


# _____________________________________


def apply_dtw(template: pd.DataFrame, test: pd.DataFrame, display=False, single_pixel=False, pixel_index: int = 0):
    r"""
    Perform DTW algorithm on template graph and test graph.

    :param template: DataFrame with ONLY one curve to be used as reference
    :param test: DataFrame with all testing curve data
    :param display: Render graph
    :param single_pixel: To perform and display DTW on single pixel. Else perform on entire test DataFrame
    :param pixel_index: which data point (pixel) to select : 0-722
    :return: Plot, Distance and optimal Path for single pixel | List with distances between reference curve and all test
             curves.
    """
    if type(template) == pd.DataFrame:
        if 'Long' in template.columns:
            starting_index = 2
        else:
            starting_index = 0

        template = template.values.tolist()[0][starting_index:]

    if single_pixel:
        test = test.values.tolist()[pixel_index][2:]

        path, distance = dtw_path(np.asarray(template), np.asarray(test), global_constraint="sakoe_chiba",
                                  sakoe_chiba_radius=3)

        if display:
            labels = ['05 Jan', '04 Feb', '01 Mar', '05 Apr', '05 May', '04 Jun', '04 Jul', '03 Aug', '02 Sep',
                      '02 Oct',
                      '01 Nov', '01 Dec']
            indexes = [0, 6, 11, 18, 24, 30, 36, 42, 48, 54, 60, 66]

            plt.plot(template, '-g', label='Template', alpha=1)
            plt.plot(test, '-r', label=f'Test : Pixel {pixel_index}', alpha=0.5)

            for entry in path:
                y_value = []
                x_value = []
                y_value.append(template[entry[0]][0])
                y_value.append(test[entry[1]])
                x_value.append(entry[0])
                x_value.append(entry[1])
                plt.plot(x_value, y_value, '--bo', alpha=0.3)

            plt.xlabel('2019')
            plt.ylabel('Band Values')
            plt.title(f"DTW Curve Comparison (DTW : {distance})")

            plt.xticks(indexes, labels, rotation=20)
            plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
            plt.legend()

            plt.show()
        return distance, path

    else:
        distance_list = []
        for row in test.iterrows():
            test = row[1][2:]
            path, distance = dtw_path(np.asarray(template), np.asarray(test), global_constraint="sakoe_chiba",
                                      sakoe_chiba_radius=3)
            distance_list.append(distance)
            print(f"Done for Data point : {row[0]}")

        if display:
            plt.bar(np.arange(len(distance_list)), distance_list)
            plt.xlabel('Pixels')
            plt.ylabel('Distance')
            plt.title('DTW Distances comparison')
            plt.axhline(y=pixel_index, label='threshold')
            plt.show()

        return distance_list


# _____________________________________


def calculate_percentile(distance_list: list, test_distance: float):
    r"""
    Calculate the percentile of the test distance against training distances.

    :param distance_list: training distances list
    :param test_distance: Distance of testing curve
    :return: Value of the percentile of testing curve
    """
    temp_data_list = distance_list.copy()
    temp_data_list.sort()

    rank = sum(i < test_distance for i in temp_data_list)
    percentile = (rank * 100) / len(distance_list)

    return percentile


# _____________________________________


def pickler(content, name_of_class: str, name_of_band: str):
    r"""
    Creates a pickle file to store the content for specific class ad band.

    :param content: Content to be pickled
    :param name_of_class: Class label
    :param name_of_band: Blue | Green | Red | NIR | SWIR | NDVI / NDWI / NDBI
    :param content_type: 'DTW' / 'all_configurations'
    :return: None
    """

    filename = os.path.abspath(__file__ + "/../../") + f"/data_2019/Pickles/{name_of_band}/DTW_{name_of_class}.dat"
    outfile = open(filename, 'wb')
    pickle.dump(content, outfile)
    outfile.close()


# _____________________________________


def unpickler(name_of_band: str, name_of_class: str):
    r"""
    Function to read DTW data from pickled file.

    :param name_of_class: Class label of requested data
    :param name_of_band: Blue | Green | Red | NIR | SWIR | NDVI / NDWI / NDBI
    :return: Dictionary with generalized curve and distances list of training samples
    """
    file_name = os.path.abspath(__file__ + "/../../") + f"/data_2019/Pickles/{name_of_band}/DTW_{name_of_class}.dat"

    infile = open(file_name, 'rb')
    pickled_content = pickle.load(infile)
    infile.close()

    return pickled_content

# _____________________________________


def create_single_pixel_df(input_data: dict, pixel_index: int):
    r"""
    Creates a DataFrame with only one pixel values.

    :param input_data: Whole DataFrame
    :param pixel_index: index of pixel chosen
    :return: DataFrame with 75 values of single pixel
    """
    single_pixel_csv = {}

    for key, value in input_data.items():
        single_pixel_csv[key] = pd.DataFrame(value.loc[pixel_index]).transpose()

    return single_pixel_csv

# _____________________________________


def trainer(input_data: pd.DataFrame, name_of_band: str, name_of_class: str = None):
    r"""
    Use training data to apply silhouette analysis on the input_data, choose the optimal configuration of clusters
    and pickle the configuration.

    :param input_data: raw input data
    :param name_of_class: Class label of requested data
    :param name_of_band: Blue | Green | Red | NIR | SWIR | NDVI / NDWI / NDBI
    :return: None
    """

    print(f"Training on : {name_of_class} - {name_of_band}")

    chosen_configuration = patternizer.patternizer(input_data=input_data, label=name_of_class, display=False)

    pickler(content=chosen_configuration, name_of_class=name_of_class, name_of_band=name_of_band)
    print(f"Pickled ! ")

# _____________________________________


def tester(test: pd.DataFrame):
    r"""
    Check the testing curve against generalised curve for every index and every class and determine its class

    :param test: The testing data cure (time-series : 73 time-points + 2 geo-reference points)
    :return: Testing DataFrame with 'label' column appended, distances DataFrame with distances from all the generalised curves.
    """
    bands = ['NDVI']
    classes = ['Agriculture', 'BarrenLand', 'Forests', 'Infrastructure', 'Water']

    test_data_frame = test.filter(['Lat', 'Long'], axis=1)

    for band in bands:
        for label in classes:
            # print(f"Checking {label} configurations")

            configuration = unpickler(name_of_class=label, name_of_band=band)
            centers_list = [x for x in configuration.cluster_centers_thresholds.values()]

            for index in range(configuration.cluster_count):
                test_distance, test_path = apply_dtw(template=centers_list[index], test=test, single_pixel=True, display=False)
                test_data_frame[f"{label}_{band}_instance {index}"] = test_distance

    test_columns = test_data_frame.columns.tolist()[2:]
    test_results = test_data_frame.values.tolist()[0][2:]
    test_label = test_columns[test_results.index(min(test_results))]

    # print(test_columns)
    # print(test_results)
    # print(test_label)
    return test_label

# _____________________________________


def dtw_training_pipeline(class_name: str):
    r"""
    Train the class from raw data

    :param class_name: class label for training
    :return: None
    """
    bands = ["NDVI"]

    start_time = time.time()
    for band in bands:
        class_name, index_of_pixel, band_name, csv_data = main.preprocess(class_name=class_name, band_name=band, pixel_index=0)
        trainer(input_data=csv_data['index files']['NDVI'], name_of_class=class_name, name_of_band=band)

    print(f"\n\n\nMODEL TRAINED FOR CLASS {class_name}")
    print(f"\t\tTOTAL TIME REQUIRED : {time.time() - start_time}")

# _____________________________________


def dtw_testing_pipeline(testing_data: pd.DataFrame = None):
    r"""
    Run the testing on entire DataFrame. If not provided, runs testing on 'test' data.

    :param testing_data: DataFrame to test
    :return: Input DataFrame with new column 'label' with testing results of every row
    """
    if testing_data is not None:
        for index in range(0, len(testing_data.index)):
            testing_df = pd.DataFrame(testing_data.iloc[index]).transpose()
            test_label = tester(testing_df)
            testing_data.loc[index, 'Label'] = test_label.split('_')[0]

    else:
        classes = ['Agriculture', 'BarrenLand', 'Forests', 'Infrastructure', 'Water']

        for class_label in classes:
            testing_data = pd.read_csv(
                    os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/test/{class_label}/preprocessed_NDVI.csv")

            mismatched_count = 0
            for index in range(0, len(testing_data.index)):
                testing_df = pd.DataFrame(testing_data.iloc[index]).transpose()
                test_label = tester(testing_df)
                testing_data.loc[index, 'Label'] = test_label.split('_')[0]

                if test_label.split('_')[0] != class_label:
                    mismatched_count += 1
                    print(f"ACTUAL : {class_label} X PREDICTED : {test_label.split('_')[0]}")

            print(f"FOR CLASS {class_label}, MISMATCHED LABELS : {mismatched_count}")
            print(f"\t\tACCURACY : {(len(testing_data.index) - mismatched_count)*100 / len(testing_data.index)}%")

    return testing_data


# Play:
# dtw_testing_pipeline()
# start_main_time = time.time()
# classes = ['Infrastructure', 'Water']
# for class_label in classes:
#     print(f"\t\t-- class {class_label} --")
#     dtw_training_pipeline(class_name=class_label)
#
# print(f"\n\n\t\t NET TIME : {time.time() - start_main_time}s")
#
# exit()
# class_name, index_of_pixel, band_name, csv_data = main.preprocess(class_name="Forests", band_name="NDVI", pixel_index=1000)
# #
# # print(class_name)
# # testing = csv_data['index files']['NDVI']
# # # #
# # trainer(input_data=testing, name_of_class='Forests', name_of_band='NDVI')
# # exit()
# zero_count = 0
# one_count = 0
# general_count = 0
#
# zero_list = []
# one_list = []
#
# for i in range(300):
#     testing_curve = create_single_pixel_df(csv_data['index files'], pixel_index=i)['NDVI']
#     value = tester(testing_curve)
# # #
#     if list(value)[-1] == '0':
#         zero_count += 1
#         zero_list.append(general_count)
#     else:
#         one_count += 1
#         one_list.append(general_count)
#     general_count += 1
#
# print(f"ZERO : {zero_count}, ONE : {one_count}")
#
# curve_203 = create_single_pixel_df(csv_data['index files'], pixel_index=203)['NDVI']
#
# forest_config = unpickler(name_of_band="NDVI", name_of_class="Forests")
# #
# color = ['b', 'g']
# for index, center in enumerate([x for x in forest_config.cluster_centers_thresholds.values()]):
#     plt.plot(center, f'-{color[index]}', label=f'instance {index}', alpha=1)
# #     distance, path = apply_dtw(center, curve_203, display=True, single_pixel=True)
# #     print(f"DISTANCE FROM {index} : {distance}")
# plt.show()
# indices = forest_config.clustered_data_indices
# clusters_instances = [x for x in forest_config.cluster_dictionary.keys()]
# clusters_objects = [x for x in forest_config.cluster_dictionary.values()]
#
# for index, instance in enumerate(clusters_instances):
#     print(f'{instance}: {clusters_objects[index].count}')
#
# print('-x-')
# print("ZERO LIST :")
# print(zero_list)
# print("ONE LIST :")
# print(one_list)
#
#
# print([x for x in indices[0]])
# print([x for x in indices[1]])
#
# print('\nNOT INITIALLY ZERO: ')
# print([x for x in zero_list if x not in [x for x in indices[0]]])
#
# print('NOT INITIALLY ONE: ')
# print([x for x in one_list if x not in [x for x in indices[1]]])
# print("++")
# print(f"Length of zero_list : {len(zero_list)}")
# print(f"Length of one_list : {len(one_list)}")
# print(f"Length of INDICE 0 : {len([x for x in indices[0]])}")
# print(f"Length of INDICE 1 : {len([x for x in indices[1]])}")

#
# plt.plot(curve_203.values.tolist()[0][2:], '--k', label='TEST', alpha=1)
#
# labels = ['05 Jan', '04 Feb', '01 Mar', '05 Apr', '05 May', '04 Jun', '04 Jul', '03 Aug', '02 Sep',
#               '02 Oct',
#               '01 Nov', '01 Dec']
# indexes = [0, 6, 11, 18, 24, 30, 36, 42, 48, 54, 60, 66]
#
# plt.xlabel('2019')
# plt.ylabel('Band Values')
# plt.title(f"Centers comparison")
#
# plt.xticks(indexes, labels, rotation=20)
# plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
# plt.legend()
# plt.show()
# general_curve = get_average_curve(csv_data['index files']['NDVI'])
#
# p, d = apply_dtw(template=general_curve, test=csv_data['index files']['NDVI'], single_pixel=False,
#                  pixel_index=index_of_pixel, display=True)
# exit()
# #
# pickled_dictionary = unpickler(name_of_class="Forests", name_of_band="NDVI")
# testing_distance, testing_path = apply_dtw(pickled_dictionary['general curve'], test=csv_data['preprocessed'],
#                                            display=True, single_pixel=True, pixel_index=index_of_pixel)
#
# exit()
# TRAINING THE DTW
# trainer(input_data['preprocessed'], class_name, band_name)

# indices = csv_data['index files']
# indices_single_pixel = create_single_pixel_df(indices, index_of_pixel)

# TESTING THE DTW
# testing_analysis = tester(indices_single_pixel)
#
# print("\nDISTANCES :")
# print(testing_analysis['distance'].to_string())
# print("\nTHRESHOLD STATUS :")
# print(testing_analysis['threshold'].to_string())
# print("\nPERCENTILE :")
# print(testing_analysis['percentile'].to_string())
#
# # To Display Distances and Thresholds :
# threshold_list = []
# bands = ['NDVI', 'NDWI', 'NDBI']
# for band in bands:
#     threshold_values = unpickler(name_of_band=band, threshold=True)
#     threshold_list.extend(threshold_values.values())
#
# distances = testing_analysis['distance'].values.tolist()[0][2:]
# names = testing_analysis['distance'].columns.tolist()[2:]
#
# color = []
#
# for index, value in enumerate(distances):
#     if value < threshold_list[index]:
#         color.append('g')
#     else:
#         color.append('r')
#
#
# fig, ax = plt.subplots()
#
# ax.stem(np.asarray([i for i in range(15)]), np.asarray(threshold_list), linefmt='k--', markerfmt='k.', use_line_collection=True)
# ax.bar(np.arange(15), distances, 0.3, color=color)
#
# plt.xticks(np.arange(15), names, rotation=20, fontsize=8)
# plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
# plt.xlabel('Curves ')
# plt.ylabel('Distance ')
# plt.title("Testing Analysis")
# plt.ylim([0, 50])
# plt.show()
# plt.close()
#
#
# # To Display Percentile :
#
# percentiles = testing_analysis['percentile'].values.tolist()[0][2:]
#
# color = ['r'] * 15
#
# for i in range(0, 15, 5):
#     minimum = percentiles.index(min(percentiles[i:i+5]))
#     color[minimum] = 'g'
#
#
# fig, ax = plt.subplots()
#
# ax.bar(np.arange(15), percentiles, 0.3, color=color)
# plt.xticks(np.arange(15), names, rotation=20, fontsize=8)
# plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
# plt.xlabel('Curves ')
# plt.ylabel('Percentile ')
# plt.title("Testing Analysis")
# plt.ylim([0, 100])
# plt.show()
# plt.close()
#

#
# file_name = os.path.abspath(
#                 __file__ + "/../../") + f"/data_2019/Pickles/{band_name}/thresholds.dat"
#
# infile = open(file_name, 'rb')
# new_dict = pickle.load(infile)
# infile.close()
#


# calculate_90_percentile()

# print(testing_distance)
# percentile_value = calculate_percentile(pickled_dictionary['distances list'], test_distance=testing_distance)
#

# plt.xlabel('NDVI (distance from GC)')
# plt.ylabel(f'NDBI (distance from GC)')
# fig, ax = plt.subplots()
#
# bands = ['NDVI', 'NDBI']
# classes = ['Forests', 'Water', 'Agriculture', 'BarrenLand', 'Infrastructure']
# color = ['green', 'blue', 'yellow', 'brown', 'black']
#
# ndvi = []
# ndwi = []
#
# for label in classes:
#     for band in bands:
#         pickled_dict = unpickler(name_of_class=label, name_of_band=band)
#         if band == 'NDVI':
#             ndvi.append(pickled_dict['distances list'])
#         else:
#             ndwi.append(pickled_dict['distances list'])
#
# for index in range(0, len(ndvi)):
#     ax.scatter(ndvi[index], ndwi[index], label=classes[index], color=color[index])
#
# ax.legend()
# plt.tight_layout()
# plt.title(f"Scatter Plot - NDVI x NDWI")
# plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
# plt.xlabel('NDVI')
# plt.ylabel('NDWI')
# plt.show()
