import cv2 as cv
import time as t
from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor

start = t.time()
#Setting up input
input = cv.imread("lfa_project/Images/apriltagTemplate.png")
height, width = input.shape[:2]

#Setting up instances
extractor = AprilTagsExtractor()
detector = BlurThresholdContourDetector()
filtrator = FilterOnConditions()
selector = HierarchicalSelector()
averagor = ColorAveragor()

#creating workflow
roi = extractor.extractRois(input)

contours = detector.detectContours(roi)

filtratedContours = filtrator.touchEdgeFilter(contours, height, width)

selectedContour = selector.selectContour(filtratedContours)

average = averagor.averageColor(input, selectedContour)

end = t.time()

print(end - start)

#creating output
cv.drawContours(input, selectedContour, -1, (0, 255, 0), 3)

#printing results
cv.imshow("result", input)
print(average)

cv.waitKey(0)

cv.destroyAllWindows()
