from tslearn.metrics import dtw
from tslearn.barycenters import dtw_barycenter_averaging


class Cluster:
    def __init__(self, data_count: int, data_points: list, instance: int):
        self.center = []
        self.count = data_count
        self.data_points = data_points
        self.instance = instance

        self.cluster_center = self.compute_center()
        self.intracluster = self.center_distance()
        # self.threshold = self.calculate_threshold()

        self.intercluster = []
        self.silhouette_list = []

    def compute_center(self):
        r"""
        Perform DTW-Barycenter Averaging Algorithm and get the centroid of the cluster.

        :return: Cluster Center curve
        """
        return dtw_barycenter_averaging(self.data_points, metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3},
                                        max_iter=3).tolist()

    def center_distance(self):
        r"""
        Get DTW distance between all the points of the cluster from the centroid of the cluster.

        :return: list of distances of all cluster data points
        """
        center_distances = []
        for point in range(self.count):
            distance = dtw(self.data_points[point], self.cluster_center,
                           global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
            center_distances.append(distance)
        return center_distances

    def compute_silhouettes(self):
        r"""
        Calculate the silhouette score for every point. Uses the formula : (B-A)/max(B, A).
        Where, B = intercluster distance. (distance from nearest cluster centroid other than the one it belongs to.)
               A = intracluster distance. (distance from its cluster centroid.)

        :return: list of silhouette scores for all the data points
        """
        silhouettes = []
        for data_index in range(self.count):
            silhouette_score = (self.intercluster[data_index] - self.intracluster[data_index]) / \
                               max(self.intercluster[data_index], self.intracluster[data_index])
            silhouettes.append(silhouette_score)

        self.silhouette_list = silhouettes

    def calculate_threshold(self):
        r"""
        Compute the 90 percentile threshold value for the distance from the cluster centroid.
        (Threshold value to classify a test data point into this cluster)

        :return:  single number between the min and max of distances list
        """
        if self.count > 1:
            distances_list = self.intracluster.copy()
            distances_list = sorted(distances_list)

            index = 0.9 * (len(distances_list) + 1)
            threshold = (index % 1) * (
                    distances_list[int(index + 1)] - distances_list[int(index)]) + distances_list[int(index)]
        else:
            threshold = self.intracluster[0]
        return threshold
