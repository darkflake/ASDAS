import pandas as pd
from data_preprocessing import main
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


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
generalized_curve = get_average_curve(band_csv)

sample_curve = band_csv.values.tolist()[band_index]

template = generalized_curve.values.tolist()[0][2:]
test = sample_curve[2:]

distance, path = fastdtw(np.asarray(template), np.asarray(test), dist=euclidean)
print(distance, path)

labels = ['05 Jan', '04 Feb', '01 Mar', '05 Apr', '05 May', '04 Jun', '04 Jul', '03 Aug', '02 Sep', '02 Oct',
          '01 Nov', '01 Dec']
indexes = [0, 6, 11, 18, 24, 30, 36, 42, 48, 54, 60, 66]

plt.plot(template, '-g', label='general', alpha=1)
plt.plot(test, '-r',  label=f'pixel {band_index}', alpha=0.5)

for entry in path:
    y_value = []
    x_value = []
    y_value.append(template[entry[0]])
    y_value.append(test[entry[1]])
    x_value.append(entry[0])
    x_value.append(entry[1])
    plt.plot(x_value, y_value, '--bo', alpha=0.3)

plt.xlabel('2019')
plt.ylabel(f'Band Value ({band_name})')
plt.title(f"Pixel: {band_index}")

plt.xticks(indexes, labels, rotation=20)
plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
plt.legend()

plt.show()
# main.display(input_data=generalized_curve, name_of_band=band_name, pixel_index=band_index, interpolate_points=None, apply_filter=False, do_interpolate=False)

# main.write_csv(input_data=generalized_curve, name_of_class=class_name, file_name=f"Generalized_{class_name}")
