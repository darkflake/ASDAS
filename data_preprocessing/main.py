import os
import pandas as pd

from data_preprocessing.interpolation import interpolate, graph

# Select Band and Data Point:
title = input("Band to plot : ")
pixel_index = int(input("Pixel Index : "))
input_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/{title}.csv")


# print(input_csv.columns.tolist())                   Get list of columns

# columnns = input_csv.columns.tolist()[2:]           Get entry for every new month for X-Axis labels
# for entry in columnns:
#     month = entry[5:7]
#     print(month)
#     if month == init_month:
#         continue
#     else:
#         labels.append(entry)
#         indexes.append(columnns.index(entry))
#         init_month = month


# Print Min & Max values for the selected data point:
print(f"Min value : {min(input_csv.values.tolist()[pixel_index][2:])} , Max value : {max(input_csv.values.tolist()[pixel_index][2:])}")


# Play:
graph(data_y=input_csv.values.tolist()[pixel_index][2:],title=str(pixel_index))
# interpolate(raw_data=input_csv.values.tolist()[pixel_index][2:], x_values=input_csv.columns.tolist(),
#             title=str(pixel_index), interpolation_points=['2019-06-04', '2019-07-19', '2019-07-19', '2019-08-23',
#                                                           '2019-08-23', '2019-09-22', '2019-09-22', '2019-10-02',
#                                                           '2019-10-17', '2019-11-06', '2019-12-11', '2019-12-31'])
