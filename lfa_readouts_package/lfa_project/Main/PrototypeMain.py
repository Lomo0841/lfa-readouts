import cv2 as cv
import time as t
from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor
from lfa_project.Utility.Printing import Printing

start = t.time()
#Setting up input
input = cv.imread("lfa_project/Images/green.png")

height, width = input.shape[:2]

#Setting up instances
printer = Printing()
extractor = AprilTagsExtractor(printer)
detector = BlurThresholdContourDetector(printer)
filtrator = FilterOnConditions(printer)
selector = HierarchicalSelector(printer)
averagor = ColorAveragor(printer)

#creating workflow
roi = extractor.extractRois(input)

contours = detector.detectContours(roi)

filtratedContours = filtrator.touchEdgeFilter(contours, height, width)

selectedContour = selector.selectContour(filtratedContours)

average = averagor.averageColor(roi, selectedContour)

end = t.time()

print(end - start)

#creating output
cv.drawContours(roi, selectedContour, -1, (0, 255, 0), 3)

#printing results
cv.imshow("result", roi)
print(average)

cv.waitKey(0)

cv.destroyAllWindows()
