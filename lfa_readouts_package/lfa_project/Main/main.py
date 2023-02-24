import cv2 as cv
import time as t

from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor

#setting up
input1 = cv.imread("lfa_project/Images/scuffedred.png")
#input2 = cv.imread("Images/testPoint.png")
height, width = input1.shape[:2]
#extractor = AprilTagsExtractor()
detector = BlurThresholdContourDetector()
filtrator = FilterOnConditions()
selector = HierarchicalSelector()
averagor = ColorAveragor()

#roi1 = extractor.extractRois(input)
#roi2 = extractor.extractRois(input)

contours = detector.detectContours(input1)
filteredContours = filtrator.touchEdgeFilter(contours, height, width)
# 1105, 645
#contours1 = filtrator.pointFilter(contours, [(1104,645)])


#filteredContours = filtrator.filterContours(contours, 100000, height, width, 10000)

chosenContour = selector.selectOutermost(filteredContours)

averagor.binaryMask(input1, chosenContour)

cv.drawContours(input1, filteredContours, -1, (0, 255, 0), 3)
cv.drawContours(input1, chosenContour, -1, (0, 0, 255), 3)
#cv.drawContours(input2, filteredContours, -1, (0, 255, 0), 3)


cv.imshow("allcontours", input1)

#cv.imshow("filteredcontours", input2)

cv.waitKey(0)

cv.destroyAllWindows()
