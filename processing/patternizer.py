from threading import Thread

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from tslearn.clustering import TimeSeriesKMeans
from processing import kmeans_config


def try_configuration(input_data: pd.DataFrame, label: str, cluster_count: int, configurations: list, index: int):
    r"""
    Apply TimeSeries-K Means algorithm on the input data for given cluster count. Store the configuration in form of
    <kmeans_Config class object> in the configurations list at index position.

    :param input_data: DataFrame consisting of the time series data
    :param label: Label of the data
    :param cluster_count: Total number of clusters to be made
    :param configurations: List of configurations to store the <kmeans_Config class object>
    :param index: location in configurations list to store
    :return: None
    """
    print(f"Working out config with {cluster_count} clusters.")
    if 'Long' in input_data.columns:
        starting_index = 2
    else:
        starting_index = 0

    data = []
    for i in range(0, len(input_data)):
        data.append(list(input_data.values.tolist()[i][starting_index:]))

    km = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw",
                          metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3})

    km_labels = km.fit_predict(data)

    config = kmeans_config.Kmeans_Config(config_label=label, input_data=input_data, cluster_count=cluster_count,
                                         data_labels=km_labels)

    configurations[index] = config


def get_optimal_configuration(config_list: list, display=False):
    r"""
    Get the silhouette scores for every configuration made and perform silhouette analysis. (Higher the score, optimal
    the clustering)

    :param config_list: List of configurations on which silhouette analysis will be performed
    :param display: Whether or not to display the silhouette scores of various configurations
    :return: Maximum silhouette score and the configuration it belongs to
    """
    silhouettes_list = []

    for config in config_list:
        silhouettes_list.append(config.cluster_silhouettes_mean)

    if display:
        color = []

        for value in silhouettes_list:
            if value == max(silhouettes_list):
                color.append('g')
            else:
                color.append('r')

        bars = plt.bar([x for x in range(2, 5)], silhouettes_list, color=color)

        for index, bar in enumerate(bars):
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, silhouettes_list[index])

        plt.xlabel('Cluster Count')
        plt.ylabel('Mean Silhouette Score')
        plt.xticks([x for x in range(2, 5)])
        plt.title('Clustering Configurations Comparison')
        plt.show()

    return max(silhouettes_list), config_list[silhouettes_list.index(max(silhouettes_list))]


def patternizer(input_data: pd.DataFrame, label: str, display=False):
    r"""
    Use parallel execution to perform silhouette analysis. Perform KMeans Algorithm with different number of clusters
    and choose the one with best silhouette score.

    :param input_data: DataFrame consisting of the time series data
    :param label: Label of the data
    :param display: Whether or not to display the silhouette scores of various configurations
    :return: Maximum silhouette score and the configuration it belongs to
    """
    configurations = [None] * 3
    threads = [None] * 3

    cluster_count = 2
    print("Analysing different configurations.")
    for i in range(len(threads)):
        threads[i] = Thread(target=try_configuration, args=(input_data, label, cluster_count, configurations, i))
        threads[i].start()
        cluster_count += 1

    for i in range(len(threads)):
        threads[i].join()
    max_silhouette, chosen_configuration = get_optimal_configuration(configurations, display=display)

    return max_silhouette, chosen_configuration
