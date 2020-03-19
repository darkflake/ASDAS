from tkinter import *

import numpy
from PIL import Image, ImageTk          # Pillow == PIL
from Image_Play import image_operations

# Create an instance of Tk which will essentially create a GUI window, and state('zoomed') will launch it in full screen
root = Tk()
root.state('zoomed')

# Variables to store input for RGB Bands and Output file name.
r_text = StringVar()
g_text = StringVar()
b_text = StringVar()
op_file_text = StringVar()

'''
DEMO ARRAYS - TO BE REPLACED WITH ACTUAL IMAGE ARRAYS.

For testing - 
                R band - all 0      (min)
                G band - all 127    (mid)
                B band - all 255    (max)
                NIR, SWIR - random between min and max

All arrays are currently hardcoded for image size 1600x600.
'''
R = numpy.zeros([600, 1600], dtype=int).reshape(600, 1600)
G = numpy.full([600, 1600], 127, dtype=int).reshape(600, 1600)
B = numpy.full([600, 1600], 255, dtype=int).reshape(600, 1600)
NIR = numpy.random.randint(0, 255, [600, 1600], dtype=int).reshape(600, 1600).reshape(600, 1600)
SWIR = numpy.random.randint(0, 255, [600, 1600], dtype=int).reshape(600, 1600).reshape(600, 1600)

# Array to pass for processing:
image_arrays = [R, G, B, NIR, SWIR]


# Function to create a preview copy of current configuration and preview on GUI:
def preview():
    # Transforming the image as per inputs:
    image_operations.transform_image(op_file_entry.get(), r_text.get(), g_text.get(), b_text.get(), image_arrays)

    # Loading the preview version created after transformation:
    preview_image_load = Image.open("preview_" + op_file_entry.get()+".png")

    # Passing the image object to image canvas to be rendered on GUI & display:
    preview_image = ImageTk.PhotoImage(preview_image_load)

    image_label.configure(image=preview_image)
    image_label.image = preview_image


# Function to save the current configuration with inputted 'output_name'
def save():
    image_operations.transform_image(op_file_entry.get(), r_text.get(), g_text.get(), b_text.get(), image_arrays, save=True)


if __name__ == "__main__":

    # Creating a frame in instance of Tk for  text boxes and input fields:
    r_frame = Frame(root)
    r_frame.pack()
    r_label = Label(r_frame, text="R:")
    r_label.pack(side=LEFT)
    r_entry = Entry(r_frame, bd=5, textvariable=r_text)
    r_entry.pack(side=LEFT)

    g_frame = Frame(root)
    g_frame.pack()
    g_label = Label(g_frame, text="G:")
    g_label.pack(side=LEFT)
    g_entry = Entry(g_frame, bd=5, textvariable=g_text)
    g_entry.pack(side=LEFT)

    b_frame = Frame(root)
    b_frame.pack()
    b_label = Label(b_frame, text="B:")
    b_label.pack(side=LEFT)
    b_entry = Entry(b_frame, bd=5, textvariable=b_text)
    b_entry.pack(side=LEFT)

    # Creating a label to load the image:
    image_label = Label(root)
    image_label.pack()

    # Frame to hold 'Output file name' option:
    op_frame = Frame(root)
    op_frame.pack()
    op_file_label = Label(op_frame, text="Output file Name: ")
    op_file_label.pack(side=LEFT)
    op_file_entry = Entry(op_frame, bd=5, textvariable=op_file_text)
    op_file_entry.insert(0, "something")
    op_file_entry.pack(side=LEFT)

    # Frame to hold 'save' and 'preview' buttons:
    button_frame = Frame(root)
    button_frame.pack()
    save_button = Button(button_frame, text="Save", command=save)
    save_button.pack(side=LEFT)
    preview_button = Button(button_frame, text="Preview", command=preview)
    preview_button.pack(side=LEFT)

    # Mainloop will actually launch the GUI
    root.mainloop()
