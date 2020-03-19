import pandas as pd
from data_preprocessing import main


def get_average_curve(input_csv: pd.DataFrame) -> pd.DataFrame:
    r"""
    Find the generalized curve to represent the class

    :param input_csv: raw class data
    :return: data points for generalized curve

    """
    average_series = input_csv.mean(axis=0)
    generalised = pd.DataFrame(average_series).transpose()
    return generalised


class_name, band_name, band_index, band_csv = main.get_data()
# interpolated_data, filtered_data = main.perform(band_csv)

generalized_curve = get_average_curve(band_csv)

main.display(input_csv=generalized_curve, name_of_band=band_name, pixel_index=band_index, interpolate_points=None, apply_filter=True, do_interpolate=False)

# main.write_csv(input_data=generalized_curve, name_of_class=class_name, file_name=f"Generalized_{class_name}")
