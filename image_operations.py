import numpy as np
import cv2

'''
Function to create an PNG image using OpenCV:

Arguments - save_name : Name to save the output file. (currently hardcoded as 'something')
            x_size, y_size : Dimensions of Satellite image.  (currently hardcoded 1600x600)
            r_array, g_array, b_array : RGB arrays to create the image.
'''


def format_save(save_name, x_size, y_size, r_array, g_array, b_array):
    r_array_form = r_array.astype(dtype='uint8')        # Any pixel value should be in 0-255 that is 8bits only.
    g_array_form = g_array.astype(dtype='uint8')
    b_array_form = b_array.astype(dtype='uint8')

    # Creating new PNG image:
    # OpenCV takes input in BGR format. Creating a new numpy array holding 3 numpy arrays of single dimension from
    # RGB arrays which are of 2 dimensions each.
    new_image = np.array([
        [b_array_form[r, c], g_array_form[r, c], r_array_form[r, c]]
        for r in range(y_size) for c in range(x_size)])

    new_image = new_image.astype(dtype='uint8')
    new_image = new_image.reshape((y_size, x_size, 3))      # Reshaping the new_image array to 1600x600x3 (RGB)
    factor = min(1200 / x_size, 600 / y_size)               # Calculating factor to scale down the image.
    new_image = cv2.resize(new_image, dsize=(0, 0), fx=factor, fy=factor)   # Reducing size to 1200x600 for display
    cv2.imwrite(save_name, new_image)                       # Actually creating a new PNG image.


'''
Function to Transform the image according to inputted parameters:

Arguments - image_name : To identify the image for saving and previewing the transformed image.
            r_text, g_text, b_text : Inputs for RGB band for new image.
            set_of_arrays : Total 5 arrays containing R,G,B,NIR,SWIR of actual image loaded.
            x_size, y_size : Dimensions of Satellite image.  (currently hardcoded 1600x600)
            save : Flag to check whether to save the current configuration or not.
'''


def transform_image(image_name, r_text, g_text, b_text, set_of_arrays=[], x_size=1600, y_size=600, save=False):

    # Splitting the set_of_arrays:
    R = set_of_arrays[0]
    G = set_of_arrays[1]
    B = set_of_arrays[2]
    NIR = set_of_arrays[3]
    SWIR = set_of_arrays[4]

    # Calculating pre-defined indexes so that they can be passed directly via GUI:
    NDVI = (NIR - R)/(NIR + R)          # Normalized Difference Vegetation Index
    NDWI = (NIR - SWIR)/(NIR + SWIR)    # Normalized Difference Water Index
    NDBI = (SWIR - NIR)/(SWIR + NIR)    # Normalized Difference Build-U[ Index

    # ---------------------------------------------------

    # Calculating what exactly is given in R,G,B input:
    # EVAL function will evaluate any expression given as parameter. ( eval(2+3) = 5 )
    # Hence, we can directly pass R+G as input to R and 'eval' will add the two numpy arrays (R,G) and return a
    # numpy array carrying the sum of R and G

    evals_rgb = [eval(r_text), eval(g_text), eval(b_text)]
    values_rgb = []

    # Creating a numpy array for new 'transformed' image:
    # ISINSTANCE will check whether first argument is of the data type passed in second argument.
    # Hence, if for any input we have a number, we will create an 2D numpy array of dimensions x_size X y_size full of
    # the inputted number. Therefore if we have 0 as input to R value, we will create a array of 1600x600 full of 0.

    for val in evals_rgb:
        if isinstance(val, int):
            values_rgb.append(np.array([[val for c in range(x_size)] for r in range(y_size)]))
        else:
            values_rgb.append(val)

    # If SAVE option is on, save the image permanently, else create a 'preview' copy which will be displayed in the GUI
    # and can be overwritten with new configurations.
    if save:
        format_save("save_"+image_name+".png", x_size, y_size, *values_rgb)
    else:
        format_save("preview_"+image_name+".png", x_size, y_size, *values_rgb)
