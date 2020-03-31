import pandas as pd
import os


def find_latest_csv(folder):
    file_list = os.listdir(f'..\\data_2019\\CSV\\{folder}')
    return file_list[-13]


def create_csv():
    temp_df = pd.DataFrame()
    classes = ['Agriculture', 'BarrenLand', 'Forests', 'Infrastructure', 'Water']
    for clas in classes:
        class_df = pd.read_csv(f"..\\data_2019\\CSV\\{clas}\\{find_latest_csv(clas)}")
        class_df['Label'] = clas
        temp_df = temp_df.append(class_df, ignore_index=True)
    temp_df.to_csv('DL_data.csv', index=False)

def refactor_csv():
    temp_df = pd.read_csv('DL_data.csv')
    final_df = pd.DataFrame()
    final_df['NDVI'] = (temp_df['B8']-temp_df['B4'])/(temp_df['B8']+temp_df['B4'])
    final_df['MNDWI'] = (temp_df['B3']-temp_df['B11'])/(temp_df['B3']+temp_df['B11'])
    final_df['NDBI'] = (temp_df['B11']-temp_df['B8'])/(temp_df['B11']+temp_df['B8'])
    final_df['Label'] = temp_df['Label']
    final_df = final_df.sample(frac=1)
    final_df.to_csv('FinalData.csv', index=False)

refactor_csv()

