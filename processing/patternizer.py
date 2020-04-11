import pandas as pd


class Cluster:
    def __init__(self, data_points: list, distances: list, barycenter: pd.DataFrame):
        self.data_points = data_points
        self.distances = distances
        self.barycenter = barycenter
        self.count = len(data_points)
        self.range = {'min': min(data_points), 'max':max(data_points)}

