from data_preprocessing import main
from processing.signal_matching import unpickler, create_single_pixel_df, apply_dtw, get_average_curve
from processing import kmeans_config
from processing import patternizer

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tslearn.metrics import soft_dtw, dtw_path, gamma_soft_dtw, cdist_dtw
from tslearn.barycenters import dtw_barycenter_averaging, dtw_barycenter_averaging_petitjean, softdtw_barycenter
from tslearn.clustering import TimeSeriesKMeans

# list1 = [[0, 0], [1, 1], [2, 2], [3, 3]]
# list2 = [[0, 0]]
#
# other_centers = [center for center in list1 if center not in list2]
# print(other_centers)
# exit()

#
# dict1 = {'a': 10, 'b': 2}
# dict2 = {'a': 1, 'b': 20}
# print([x for x in dict1.keys()])
# exit()
# df1 = pd.DataFrame.from_dict(dict1, orient='index')
# df2 = pd.DataFrame.from_dict(dict2, orient='index')
#
# df1 = pd.concat([df1, df2], axis=1)
# print(sum(df1.values.tolist()[0]))
#
# print(df1)
# exit()

# y = np.array([5, 30, 20, 10, 40, 50, 100, 50])
# my_colors = ['brown','pink', 'red', 'green', 'blue', 'cyan','orange','purple']
# plt.bar(range(len(y)), y, color=my_colors)
# plt.legend()
# plt.show()
# exit()

unpickled = unpickler(name_of_band='NDVI', name_of_class='Infrastructure')

class_name, index_of_pixel, band_name, csv_data = main.preprocess()

indices = csv_data['index files']
pixel_1 = create_single_pixel_df(indices, index_of_pixel)['NDVI']
pixel_10 = create_single_pixel_df(indices, index_of_pixel + 100)['NDVI']
pixel_50 = create_single_pixel_df(indices, index_of_pixel + 500)['NDVI']
pixel_100 = create_single_pixel_df(indices, index_of_pixel + 700)['NDVI']

combined = pixel_1.append(pixel_10, ignore_index=True)
combined = combined.append(pixel_50, ignore_index=True)
combined = combined.append(pixel_100, ignore_index=True)

forest_ndvi = indices['NDVI']

maxed, chosen_cluster = patternizer.patternizer(input_data=forest_ndvi, label='forest', display=True)
print(maxed)
print(chosen_cluster.cluster_count)
exit()

general = get_average_curve(combined).values.tolist()[0]

color_dict = {0: 'r', 1: 'g', 2: 'b'}

# dis_fast, pat_fast = apply_dtw(unpickled['general curve'], create_single_pixel_df(indices, index_of_pixel+554)['NDVI'],
# display=True, single_pixel=True, fast=True)

# dis, pat = apply_dtw(unpickled['general curve'], create_single_pixel_df(indices, index_of_pixel+554)['NDVI'],
# display=True, single_pixel=True, fast=False)

# exit()

plt.figure(1)
labels = ['05 Jan', '04 Feb', '01 Mar', '05 Apr', '05 May', '04 Jun', '04 Jul', '03 Aug', '02 Sep', '02 Oct', '01 Nov',
          '01 Dec']
indexes = [0, 6, 11, 18, 24, 30, 36, 42, 48, 54, 60, 66]
plt.xlabel('2019')
plt.ylabel(f'Band Values ')
plt.title(f"DTW Curve Comparison")
plt.xticks(indexes, labels, rotation=20)
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

# plt.plot(np.asarray(general), '--k', label='Mean', alpha=0.5)
# plt.legend()

dataset = []
for i in range(0, 4):
    dataset.append(list(combined.values.tolist()[i][2:]))

# columns = combined.columns
# new_df = pd.DataFrame(dataset, columns=columns[2:])
#
# print(combined)
# print(dataset)
# print(new_df)
# exit()

# dtw_bary_2 = dtw_barycenter_averaging(dataset[1:4],
#                                       metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
#                                       max_iter=3)

path, tslearn_distance_1 = dtw_path(np.asarray(general), np.asarray(pixel_1), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
print(path)
print(tslearn_distance_1)
exit()

for j in range(3):
    sil_list = []
    config_list = []
    for i in range(2, 4):
        km = TimeSeriesKMeans(n_clusters=i, metric="dtw",
                              metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3}).fit(dataset)

        km_labels = km.predict(dataset)
        print(f"\n\nFor {i} CLusters, DISTRIBUTION : {km_labels}")

        config = kmeans_config.Kmeans_Config(label='Forests', input_data=combined, cluster_count=i,
                                             data_labels=km_labels)
        config.visualize()
        config_list.append(config)

    for configuration in config_list:
        sil_list.append(configuration.cluster_silhouettes_mean)
    print("\n================== ## ==================\n")

    print(
        f"FOR BEST SCORE CHOSE CONFIGURATION WITH == {config_list[sil_list.index(max(sil_list))].cluster_count} CLUSTERS")



# plt.plot(np.asarray(out_clusters_list[2]), f'--g', label='Test : Pixel 2', alpha=0.5)
# plt.plot(np.asarray(out_clusters_list[7]), f':g', label='Test : Pixel 7', alpha=0.5)
#
# plt.plot(np.asarray(out_clusters_list[3]), f'--b', label='Test : Pixel 3', alpha=0.5)
# plt.plot(np.asarray(out_clusters_list[8]), f':b', label='Test : Pixel 8', alpha=0.5)
#
# plt.plot(np.asarray(out_clusters_list[2]), f'--m', label='Test : Pixel 4', alpha=0.5)
# plt.plot(np.asarray(out_clusters_list[7]), f':m', label='Test : Pixel 9', alpha=0.5)

# plt.plot(np.asarray(km.cluster_centers_[0]), ':r', label='cluster center 1', alpha=1)
# plt.plot(np.asarray(km.cluster_centers_[1]), ':g', label='cluster center 2', alpha=1)


# dtw_bary_1 = dtw_barycenter_averaging(dataset[0], metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
#                                     max_iter=3)
#
#
# dtw_bary_2 = dtw_barycenter_averaging(dataset[1:4], metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
#                                     max_iter=3)


#
plt.legend()
#
# for entry in [x for x in path]:
#     y_value = []
#     x_value = []
#     y_value.append(pixel_1[entry[0]])
#     y_value.append(pixel_10[entry[1]])
#     x_value.append(entry[0])
#     x_value.append(entry[1])
#     plt.plot(x_value, y_value, '--bo', alpha=0.3)
#
# plt.legend()
# #
# #
#
# mat_x_value = []
# mat_y_value = []
# for entry in [x for x in path]:
#     print(entry)
#     mat_y_value.append(entry[0])
#     mat_x_value.append(entry[1])
#
# plt.figure(2)
# plt.plot(np.asarray(mat_x_value).T, np.asarray(mat_y_value).T, '-b', alpha=1)
# # plt.plot(np.asarray(mat_y_value).T, np.asarray(mat_x_value).T, '-g', alpha=1)
#
# plt.plot([0, 72], [0, 72], ':k', alpha = 0.3)
# plt.xlabel("Pixel 10")
# plt.ylabel("Pixel 1")
#
# plt.xticks(np.arange(73), range(73))
# plt.yticks(np.arange(73), range(73))
# plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.25)
#
# plt.tight_layout()
# ____
#
# pixel_1_distances = []
# pixel_10_distances = []
#
# dtw_distance_1, path_1 = fastdtw.dtw(np.asarray(general), np.asarray(pixel_1), dist=euclidean)
# dtw_distance_10, path_10 = fastdtw.dtw(np.asarray(general), np.asarray(pixel_10), dist=euclidean)
#
# dtw_distance_1_bary, path_1_bary = fastdtw.dtw(np.asarray(dtw_bary), np.asarray(pixel_1), dist=euclidean)
# dtw_distance_10_bary, path_10_bary = fastdtw.dtw(np.asarray(dtw_bary), np.asarray(pixel_10), dist=euclidean)
#
# pixel_1_distances.append(dtw_distance_1)
# pixel_10_distances.append(dtw_distance_1_bary)
# pixel_1_distances.append(dtw_distance_10)
# pixel_10_distances.append(dtw_distance_10_bary)
#
# path, tslearn_distance_1 = dtw_path(np.asarray(general), np.asarray(pixel_1), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
# d_path, tslearn_distance_10 = dtw_path(np.asarray(general), np.asarray(pixel_10), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)


# path_bary, tslearn_distance_1_bary = dtw_path(np.asarray(dtw_bary), np.asarray(pixel_1), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
# d_path_bary, tslearn_distance_10_bary = dtw_path(np.asarray(dtw_bary), np.asarray(pixel_10), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
#
# pixel_1_distances.append(tslearn_distance_1)
# pixel_10_distances.append(tslearn_distance_1_bary)
#
# pixel_1_distances.append(tslearn_distance_10)
# pixel_10_distances.append(tslearn_distance_10_bary)
#
#
# plt.figure(2)
# labels_2 = ["FastDTW-Pixel 1", "FastDTW-Pixel 10", "DTW-Pixel 1", "DTW-Pixel 10"]
# indexes_2 = np.arange(len(labels_2))
# plt.xlabel('Algorithm')
# plt.ylabel(f'Distance')
# plt.title(f"DTW Algorithm Comparison")
# width = 0.35
# plt.xticks(indexes_2, labels_2)
# plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
#
# bar_1 = plt.bar(indexes_2 - width/2, pixel_1_distances, width, label='Mean')
# bar_2 = plt.bar(indexes_2 + width/2, pixel_10_distances, width, label='DTW-Barycenter')
#
#
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         plt.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
#
#
# autolabel(bar_1)
# autolabel(bar_2)
# plt.tight_layout()
# plt.legend()
#
#
# plt.figure(3)
# labels_2 = ["FastDTW-Mean", "DTW-Mean", "FastDTW-Bary", "DTW-Bary"]
# indexes_2 = np.arange(len(labels_2))
# plt.xlabel('Algorithm')
# plt.ylabel(f'Distance Ratio : 1x10')
# plt.title(f"DTW Algorithm Comparison (Ratio)")
# plt.xticks(indexes_2, labels_2)
# plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
#
# ratio = []
# for index in range(0, len(pixel_1_distances), 2):
#     ratio.append(pixel_1_distances[index]/pixel_1_distances[index+1])
#
# for index in range(0, len(pixel_10_distances), 2):
#     ratio.append(pixel_10_distances[index] / pixel_10_distances[index + 1])
#
# print(f"PIXEL 1 : {pixel_1_distances}")
# print(f"PIXEL 10 : {pixel_10_distances}")
# print(f"RATIOS : {ratio}")
# plt.bar(np.arange(len(ratio)), ratio, width=0.1)


plt.show()
