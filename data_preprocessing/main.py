import os
import pandas as pd

from data_preprocessing.interpolation import interpolate, graph


# Handling Nan Values:
def fix_nan(unprocessed: pd.DataFrame):
    total_nan = unprocessed.isna().sum().sum()                                                                          # Check if there are NaN
    print(f"Total NaN values : {total_nan}")

    if total_nan > 0:
        print("Interpolating Nan Values..")
        processed = unprocessed.interpolate(method='linear', axis=1, inplace=False, limit_direction='both')             # Interpolate
        return processed
    else:
        return unprocessed


def get_data():
    band_name = input("Band to plot : ")
    pixel_index = int(input("Pixel Index : "))

    input_csv = pd.read_csv(os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{band_name}.csv")                  # Get csv
    return band_name, pixel_index, input_csv


# Play:
band_name, index, csv = get_data()
no_nan_csv = fix_nan(csv)

no_nan_csv.to_csv(os.path.abspath(__file__ + "/../../") + f"/data_2019/csv/{band_name}.csv", index=False)

# Print Min & Max values for the selected data point:
print(f"Min value : {min(no_nan_csv.values.tolist()[index][2:])} , Max value : {max(no_nan_csv.values.tolist()[index][2:])}")

# graph(data_y=no_nan_csv.values.tolist()[index][2:], band=band_name, title=str(index))
interpolated_data = interpolate(raw_data=no_nan_csv.values.tolist()[index][2:], display=True, apply_filter=True,
                                x_values=no_nan_csv.columns.tolist(), band=band_name, title=str(index),
                                interpolation_points=['2019-06-04', '2019-07-19', '2019-07-19', '2019-08-23',
                                                      '2019-08-23', '2019-09-22', '2019-09-22', '2019-10-02',
                                                      '2019-10-17', '2019-11-06', '2019-12-11', '2019-12-31'])


# _____________________________________________________________________________________________________________________
# print(no_nan_csv.columns.tolist())                   Get list of columns

# columnns = no_nan_csv.columns.tolist()[2:]           Get entry for every new month for X-Axis labels
# for entry in columnns:
#     month = entry[5:7]
#     print(month)
#     if month == init_month:
#         continue
#     else:
#         labels.append(entry)
#         indexes.append(columnns.index(entry))
#         init_month = month
