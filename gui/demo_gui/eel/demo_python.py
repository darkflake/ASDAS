
import os
import eel
import cv2 as cv
import datetime
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt


eel.init('web')
@eel.expose
def piechart():
    df=pd.read_csv('6580631000-1547012631000.csv')
    country_data = df["index"]
    medal_data = df["B11"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b"]
    plt.pie(medal_data, labels=country_data,autopct='%1.1f%%')
    plt.title('My Tasks')
    plt.show()



'''
# Data to plot
labels = 'Python', 'C++', 'Ruby', 'Java'
sizes = [215, 130, 245, 210]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0, 0)  # explode 1st slice


def plot_piechart():
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()

    per1 = pd.date_range(start='1-1-2018',
                     end='1-05-2018', freq='5H')

for val in per1:
    print(val)


def   show_image():
    img=cv.imread('walpaper.jpg')
    cv.imshow('IMAGE',img)
    cv.waitKey(0)
    cv.destroyAllWindows()


    #img = Image.open('C:/Users/HP/Pictures/eth.PNG')
    #img.show()
    # os.startfile('C:/Users/HP/Pictures/Saved Pictures/walpaper.jpg')
'''





eel.start('demo_html.html')


