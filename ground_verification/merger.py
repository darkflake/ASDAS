import pandas as pd


def merge(label):
    actual_df = pd.read_csv(f"B4-B8 _ 1-1_23-2_{label}.csv", float_precision='round_trip', dtype='str')
    verification_df = pd.read_csv(f"ground_verification_{label}.csv", float_precision='round_trip', dtype='str')

    actual_df.columns = ['system:index', 'B4', 'B8', 'long', 'lat']

    actual_df.sort_values(by=['lat', 'long'], inplace=True)
    actual_df.reset_index(inplace=True)

    verification_df.sort_values(by=['lat', 'long'], inplace=True)
    verification_df.reset_index(inplace=True)

    # max_long = actual_df['lat'].max()
    # min_long = actual_df['lat'].min()
    # print(max_long)
    # print(min_long)
    # print((float(max_long) - float(min_long)) * 1000000)
    # exit()

    actual_list = []
    actual_pointer = 0
    index = 0
    # for index in verification_df.index:
    #     actual_lat, actual_long = get_actual(actual_pointer, actual_df)
    #
    #     while float(verification_df['lat'][index]) == actual_lat and float(verification_df['long'][index]) == actual_long:
    #         print("in while")
    #         actual_list.append(actual_pointer)
    #         actual_pointer += 1
    #         actual_lat, actual_long = get_actual(actual_pointer, actual_df)
    #
    # for index in verification_df.index:
    #     actual_lat, actual_long = get_actual(actual_pointer, actual_df)

    while True:
        ver_lat = round(float(verification_df['lat'][index]), 4)
        ver_long = round(float(verification_df['long'][index]), 4)
        actual_lat, actual_long = get_actual(actual_pointer, actual_df)

        print(index)
        print("ap : " + str(actual_pointer))
        print("a : " + str(actual_lat) + ", " + str(actual_long))
        print("v : " + str(ver_lat) + ", " + str(ver_long))

        if actual_lat < ver_lat:
            actual_pointer += 1
            continue
        elif ver_lat == actual_lat and actual_long < ver_long:
            actual_pointer += 1
            continue
        elif ver_lat == actual_lat and ver_long == actual_long:
            print("a" + str(actual_pointer))
            actual_pointer += 1
            actual_list.append(actual_pointer)
        elif ver_lat == actual_lat and actual_long > ver_long:
            actual_pointer += 1
            continue
        elif actual_lat > ver_lat:
            index += 1
            if index == 20:
                break
            continue



        # while float(verification_df['lat'][index]) < actual_lat:
        #     actual_pointer += 1
        #     continue
        # while float(verification_df['long'][index]) < actual_long:
        #     actual_pointer += 1
        #     continue
        # while float(verification_df['lat'][index]) == actual_lat and float(verification_df['long'][index]) == actual_long:
        #     print("in while")
        #     actual_list.append(actual_pointer)
        #     actual_pointer += 1
        #     actual_lat, actual_long = get_actual(actual_pointer, actual_df)

    return actual_list


def get_actual(pointer, data_frame):
    actual_lat = round(float(data_frame['lat'][pointer]), 4)
    actual_long = round(float(data_frame['long'][pointer]), 4)
    # print(actual_lat, actual_long)
    return actual_lat, actual_long


print(merge('vegetation'))
