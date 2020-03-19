import os
import pandas as pd
from datetime import datetime

lat_long_list = []
bands_List = ["Blue", "Green", "Red", "NIR", "NDVI", "SWIR", "SCL"]


'''
CODE TO CREATE BASIC BAND CSVs WITH LAT-LONG FOR 30 POINTS :
# -------------------------------------------------------------
csv_for_pos = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/1546580631000-1547012631000.csv")
geo_frame = pd.DataFrame(csv_for_pos['.geo'])

for row in geo_frame.iterrows():
    long, lat = (row[1][0][31:-3]).split(",")
    lat_long_list.append([lat, long])

new_geo_df = pd.DataFrame(data=lat_long_list, columns=["Lat", "Long"])
for band in bands_List:
    new_geo_df.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/" + band + ".csv", index=False)

'''

start_date = 1546580631000
Blue_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/Blue.csv")
Green_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/Green.csv")
Red_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/Red.csv")
NIR_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/NIR.csv")
NDVI_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/NDVI.csv")
SWIR_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/SWIR.csv")
SCL_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/SCL.csv")


def get_time(epoch: int):
    return datetime.fromtimestamp(epoch/1000).strftime('%Y-%m-%d')


for img in range(1, 74):
    if img > 1:
        start_date = 1546580631000 + (img - 1) * 432000000
    end_date = start_date + 432000000

    filename = str(start_date) + "-" + str(end_date)
    image_date = get_time(start_date+86400000)
    print(f"Done for {image_date}")

    input_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/" + filename + ".csv")

    Blue_csv[str(image_date)] = input_csv["B2"]
    Green_csv[str(image_date)] = input_csv["B3"]
    Red_csv[str(image_date)] = input_csv["B4"]
    NIR_csv[str(image_date)] = input_csv["B8"]
    NDVI_csv[str(image_date)] = ((input_csv["B8"] - input_csv["B4"]) / (input_csv["B8"] + input_csv["B4"]))
    SWIR_csv[str(image_date)] = input_csv["B11"]
    SCL_csv[str(image_date)] = input_csv["SCL"]

    Blue_csv.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/Blue.csv", index=False)
    Green_csv.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/Green.csv", index=False)
    Red_csv.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/Red.csv", index=False)
    NIR_csv.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/NIR.csv", index=False)
    NDVI_csv.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/NDVI.csv", index=False)
    SWIR_csv.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/SWIR.csv", index=False)
    SCL_csv.to_csv(os.path.abspath(__file__ + "/../../")+"/data_2019/csv/Forests/SCL.csv", index=False)
