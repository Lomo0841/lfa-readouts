import cv2 as cv
import time as t
from lfa_project.Utility.Printer import Printing

printer = Printing()

cam = cv.VideoCapture(0)

t.sleep(5)

for i in range(10):
    ret, inputImage = cam.read()

    printer.write_image(inputImage, str(i))

    t.sleep(1)

cam.release()  

