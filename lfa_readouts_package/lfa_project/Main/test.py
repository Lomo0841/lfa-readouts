import cv2 as cv
import time as t
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Utility.Printing import Printing

#setting up instances
printer = Printing()

thresh = BlurThresholdContourDetector(printer)

#program
input = cv.imread("lfa_project/Images/green.png")

thresh.detectContours(input)

cv.imshow("input", input)

#finishing
cv.waitKey(0)
cv.destroyAllWindows()
