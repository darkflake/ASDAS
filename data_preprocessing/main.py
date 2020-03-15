import os
import pandas as pd

from data_preprocessing.interpolation import graph

Green_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/NIR.csv")

# print(Blue_csv.values.tolist()[0])
# print(list(Blue_csv))

graph(Green_csv.values.tolist()[1][2:], list(Green_csv))