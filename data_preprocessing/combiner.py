import os
import pandas as pd
from datetime import datetime
import time


def create_new_csv(name_of_class: str, get_geo_df=False):
    r"""
    Create base CSVs per band and index with just geo-information (Lat-Long)

    :param name_of_class: Class label of data
    :param get_geo_df: Just return the DataFrame with Lat-long
    :return: None
    """
    lat_long_list = []
    bands_list = ["Blue", "Green", "Red", "NIR", "SWIR", "SCL", "NDVI", "NDBI", "NDWI"]
    csv_for_pos = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/1546580631000"
                                                                    "-1547012631000.csv")
    geo_frame = pd.DataFrame(csv_for_pos['.geo'])

    for row in geo_frame.iterrows():
        long, lat = (row[1][0][31:-3]).split(",")
        lat_long_list.append([lat, long])

    new_geo_df = pd.DataFrame(data=lat_long_list, columns=["Lat", "Long"])

    if get_geo_df:
        return new_geo_df

    for band in bands_list:
        new_geo_df.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/" + band + ".csv",
                          index=False)


def get_time(epoch: int):
    return datetime.fromtimestamp(epoch/1000).strftime('%Y-%m-%d')


def combine(name_of_class: str):
    r"""
    Combine image data of all bands into band wise time series data for whole year

    :param name_of_class: Class label of data
    :return: None
    """
    print(f'== Creating band & index CSVs for class : {name_of_class} ==')
    start_time = time.time()

    create_new_csv(name_of_class=name_of_class)

    start_date = 1546580631000

    Blue_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/Blue.csv")
    Green_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/Green.csv")
    Red_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/Red.csv")
    NIR_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NIR.csv")
    SWIR_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/SWIR.csv")
    SCL_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/SCL.csv")
    NDVI_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NDVI.csv")
    NDBI_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NDBI.csv")
    NDWI_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NDWI.csv")

    print(f"Scanning satellite image feed for year 2019")
    for img in range(1, 74):
        if img > 1:
            start_date = 1546580631000 + (img - 1) * 432000000
        end_date = start_date + 432000000

        filename = str(start_date) + "-" + str(end_date)
        image_date = get_time(start_date+86400000)
        print(f"Done for {image_date}")

        input_csv = pd.read_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/" + filename + ".csv")

        Blue_csv[str(image_date)] = input_csv["B2"]
        Green_csv[str(image_date)] = input_csv["B3"]
        Red_csv[str(image_date)] = input_csv["B4"]
        NIR_csv[str(image_date)] = input_csv["B8"]
        SWIR_csv[str(image_date)] = input_csv["B11"]
        SCL_csv[str(image_date)] = input_csv["SCL"]
        NDVI_csv[str(image_date)] = ((input_csv["B8"] - input_csv["B4"]) / (input_csv["B8"] + input_csv["B4"]))
        NDBI_csv[str(image_date)] = ((input_csv["B11"] - input_csv["B8"]) / (input_csv["B11"] + input_csv["B8"]))
        NDWI_csv[str(image_date)] = ((input_csv["B8"] - input_csv["B11"]) / (input_csv["B8"] + input_csv["B11"]))

        Blue_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/Blue.csv", index=False)
        Green_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/Green.csv", index=False)
        Red_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/Red.csv", index=False)
        NIR_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NIR.csv", index=False)
        SWIR_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/SWIR.csv", index=False)
        SCL_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/SCL.csv", index=False)
        NDVI_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NDVI.csv", index=False)
        NDBI_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NDBI.csv", index=False)
        NDWI_csv.to_csv(os.path.abspath(__file__ + "/../../")+f"/data_2019/csv/{name_of_class}/NDWI.csv", index=False)
    print("Combined!\n")
    print(f"\t\tTOTAL TIME REQUIRED : {time.time() - start_time}\n")

# PLAY:
# combine(input("Enter Class :"))

