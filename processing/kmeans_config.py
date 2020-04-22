import pandas as pd
import statistics
from collections import defaultdict

import processing.cluster as cluster
from tslearn.metrics import dtw


def get_cluster_indices(data_labels):
    r"""
    Get the indices of data points for every cluster instance.

    :return: dictionary with indices list for instance key
    """
    clustered_points = defaultdict(list)

    for index, label in enumerate(data_labels):
        clustered_points[label].append(index)

    return clustered_points


class Kmeans_Config:
    def __init__(self, config_label: str, input_data: pd.DataFrame, cluster_count: int, data_labels: list):
        self.label = config_label
        self.input_data = input_data.drop(['Lat', 'Long'], axis=1, inplace=False)

        self.cluster_count = cluster_count

        self.clustered_data_indices = get_cluster_indices(data_labels)
        self.clustered_data_points = self.get_cluster_data()
        self.cluster_dictionary = self.create_clusters()
        self.cluster_centers_thresholds = self.get_cluster_centers()

        self.cluster_silhouettes_list, self.cluster_silhouettes_mean = self.get_silhouettes()

    def get_cluster_data(self):
        r"""
        Based on the indices, get the actual data points from input_data.

        :return: dictionary with data points for instance key
        """
        cluster_data_points = {}
        for label, data in self.clustered_data_indices.items():
            points_list = []
            for index in data:
                points_list.append(self.input_data.values.tolist()[index])
            cluster_data_points[label] = points_list
        return cluster_data_points

    def create_clusters(self):
        r"""
        Create <'Clusters' class object> for all clusters in configuration.

        :return: dictionary with <'Clusters' class object> for instance key
        """
        clusters = {}
        for label, data in self.clustered_data_indices.items():
            new_cluster = cluster.Cluster(data_count=len(data),
                                          data_points=self.clustered_data_points[label], instance=label)
            clusters[label] = new_cluster
        return clusters

    def get_cluster_centers(self):
        r"""
        Get the cluster centroids for all clusters in the configuration.

        :return: list with cluster centers in order of instances
        """
        centers = {}
        for index in range(self.cluster_count):
            current_cluster = self.cluster_dictionary[index]
            centers[index] = current_cluster.cluster_center
        return centers

    def compute_intercluster(self):
        r"""
        Compute the intercluster scores  for every point in all clusters. (DTW distance from the cluster centroid of
        closest cluster except the one it belongs to) and assign the list to the 'intercluster' variable of that cluster.

        :return: None
        """
        for index in range(self.cluster_count):
            current_cluster = self.cluster_dictionary[index]
            other_centers = [center for center in [x for x in self.cluster_centers_thresholds.values()] if center not in [current_cluster.cluster_center]]

            remote_distances = []
            for point in current_cluster.data_points:
                other_distances = []

                for other_center in other_centers:
                    dtw_distance = dtw(point, other_center, global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
                    other_distances.append(dtw_distance)

                remote_distances.append(min(other_distances))

            current_cluster.intercluster = remote_distances
            other_centers.clear()

    def get_silhouettes(self):
        r"""
        Invoke the 'compute_silhouette()' method for each cluster and get the score. Calculate the mean silhouette
        score of all the clusters which represents the silhouette score of the configurations.

        :return: list of silhouette scores and mean silhouette score
        """
        silhouette_scores = {}
        silhouette_scores_list = []

        self.compute_intercluster()

        for index in range(self.cluster_count):
            current_cluster = self.cluster_dictionary[index]
            current_cluster.compute_silhouettes()
            silhouette_scores[index] = current_cluster.silhouette_list
            silhouette_scores_list.extend(current_cluster.silhouette_list)
        return silhouette_scores_list, statistics.mean(silhouette_scores_list)

    def visualize(self):
        r"""
        Print a detailed description about the configuration.

        :return: The DataFrame with details.
        """
        config_df = pd.DataFrame()

        for point_index in range(self.cluster_count):
            details = {'Cluser Instance': self.cluster_dictionary[point_index].instance,

                       'Total Data Points': self.cluster_dictionary[point_index].count,

                       'Cluster Average Silhouette Score': [
                           statistics.mean(self.cluster_dictionary[point_index].silhouette_list)],

                       'Data points below Configuration Silhouette Score': len(
                           [x for x in self.cluster_dictionary[point_index].silhouette_list if
                            x < self.cluster_silhouettes_mean])}

            cluster_df = pd.DataFrame.from_dict(details, orient='index')

            config_df = pd.concat([config_df, cluster_df], axis=1)

        print(config_df.to_string())
        print("__ __")
        print(f"Total Clusters : {self.cluster_count}")
        print(f"Configuration Silhouettes Mean : {self.cluster_silhouettes_mean}")
        print(f"Total points below Configuration Silhouettes Mean : {sum(config_df.values.tolist()[3])}")
        return config_df
