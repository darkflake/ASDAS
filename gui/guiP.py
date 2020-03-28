import eel
import cv2 as cv
eel.init('web')
@eel.expose
def show():
     img=cv.imread("C:/Users/RUPALI SHIVPURE/Downloads/water.jpg", 1)
     cv.imshow('image',img)
     cv.waitKey(0)
     #cv.destroyAllWindows()
eel.start('gui.html')