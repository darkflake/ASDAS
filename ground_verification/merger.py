import pandas as pd


def merge(label):
    actual_df = pd.read_csv(f"B4-B8 _ 1-1_23-2_{label}.csv", float_precision='round_trip', dtype='str')
    verification_df = pd.read_csv(f"ground_verification_{label}.csv", float_precision='round_trip', dtype='str')

    actual_df.columns = ['system:index', 'B4', 'B8', 'long', 'lat']

    actual_df.sort_values(by=['lat', 'long'], inplace=True)
    actual_df.reset_index(inplace=True)

    verification_df.sort_values(by=['lat', 'long'], inplace=True)
    verification_df.reset_index(inplace=True)

    actual_pointer = 0
    actual_list = []

    for index in verification_df.index:
        actual_pointer = actual_list[-1]


merge('vegetation')
