from data_preprocessing import main
from processing.signal_matching import unpickler, create_single_pixel_df, apply_dtw, get_average_curve

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

from tslearn.metrics import soft_dtw, dtw_path, gamma_soft_dtw, cdist_dtw
from tslearn.barycenters import dtw_barycenter_averaging, dtw_barycenter_averaging_petitjean, softdtw_barycenter
from tslearn.clustering import TimeSeriesKMeans
import fastdtw

unpickled = unpickler(name_of_band='NDVI', name_of_class='Forests')

class_name, index_of_pixel, band_name, csv_data = main.preprocess()

indices = csv_data['index files']
pixel_1 = create_single_pixel_df(indices, index_of_pixel)['NDVI']
pixel_10 = create_single_pixel_df(indices, index_of_pixel+100)['NDVI']
pixel_50 = create_single_pixel_df(indices, index_of_pixel+500)['NDVI']
pixel_100 = create_single_pixel_df(indices, index_of_pixel+700)['NDVI']


combined = pixel_1.append(pixel_10, ignore_index=True)
combined = combined.append(pixel_50, ignore_index=True)
combined = combined.append(pixel_100, ignore_index=True)

general = get_average_curve(combined).values.tolist()[0][2:]

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

km = TimeSeriesKMeans(n_clusters=3, metric="dtw",
                      metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3}, verbose=1).fit(dataset)

km_labels = km.predict(dataset)
print(km_labels)
print(km.inertia_)
print(km.n_iter_)

plt.plot(np.asarray(dataset[0]), f'-{color_dict[km_labels[0]]}', label='Test : Pixel 1', alpha=0.3)
plt.plot(np.asarray(dataset[1]), f'-{color_dict[km_labels[1]]}', label='Test : Pixel 10', alpha=0.3)
plt.plot(np.asarray(dataset[2]), f'-{color_dict[km_labels[2]]}', label='Test : Pixel 50', alpha=0.3)
plt.plot(np.asarray(dataset[3]), f'-{color_dict[km_labels[3]]}', label='Test : Pixel 100', alpha=0.3)

plt.plot(np.asarray(km.cluster_centers_[0]), ':r', label='cluster center 1', alpha=1)
plt.plot(np.asarray(km.cluster_centers_[1]), ':g', label='cluster center 2', alpha=1)
plt.plot(np.asarray(km.cluster_centers_[2]), ':b', label='cluster center 2', alpha=1)


dtw_bary_1 = dtw_barycenter_averaging(dataset[0], metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
                                    max_iter=3)


dtw_bary_2 = dtw_barycenter_averaging(dataset[1:3], metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
                                    max_iter=3)

dtw_bary_3 = dtw_barycenter_averaging(dataset[3], metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
                                    max_iter=3)


path, distance_10 = dtw_path(dtw_bary_2, np.asarray(pixel_10), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
path_50, distance_50 = dtw_path(dtw_bary_2, np.asarray(pixel_50), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
print(f'bary distance : {distance_10} - {distance_50}')

c_path, c_distance_10 = dtw_path(km.cluster_centers_[1], np.asarray(pixel_10), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
c_path_50, c_distance_50 = dtw_path(km.cluster_centers_[1], np.asarray(pixel_50), global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
print(f'center distance : {c_distance_10} - {c_distance_50}')

#
plt.plot(np.asarray(dtw_bary_1), f'--{color_dict[km_labels[0]]}', label='DTW-Barycenter for cluster 1', alpha=0.5)
plt.plot(np.asarray(dtw_bary_2), f'--{color_dict[km_labels[1]]}', label='DTW-Barycenter for cluster 2', alpha=0.5)
plt.plot(np.asarray(dtw_bary_3), f'--{color_dict[km_labels[3]]}', label='DTW-Barycenter for cluster 3', alpha=0.5)
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
#
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
