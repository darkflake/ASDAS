
import os
import eel
import cv2 as cv
import datetime
from PIL import Image


eel.init('web')
@eel.expose

def   show_image():
    img=cv.imread('walpaper.jpg')
    cv.imshow('IMAGE',img)
    cv.waitKey(0)
    cv.destroyAllWindows()


    #img = Image.open('C:/Users/HP/Pictures/eth.PNG')
    #img.show()
    # os.startfile('C:/Users/HP/Pictures/Saved Pictures/walpaper.jpg')


'''
eel.expose()
def write():
    str="this is demo project"
    print(str)'''





eel.init('web', allowed_extensions=['.js', '.html'])

eel.init('web')
@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)


say_hello_py('Python World!')
#eel.say_hello_js('Python World!')   # Call a Javascript function

@eel.expose
def date():

    x = datetime.datetime.now()

    print(x.year)


eel.start('demo_html.html', mode='chrome app')


