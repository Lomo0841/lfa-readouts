import cv2 as cv
import time as t
import platform 
from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor
from lfa_project.Utility.Printing import Printing
from lfa_project.Implementations.Context import Context

imageName = "orange.png"

if platform.system() == 'Windows':
    inputImage = cv.imread("lfa_readouts_package\lfa_project\Images\\" + imageName)
else:
    inputImage = cv.imread("lfa_project/Images/" + imageName)

height, width = inputImage.shape[:2]

#Setting up instances
context = Context()

printer = Printing()
#THIS SHOULD BE OUTSOURCED TO THE TAKE PICTURE CLASS
printer.write_image(inputImage, "OriginalImage")

context.roiExtractorStrategy = AprilTagsExtractor(printer, inputImage)
roi = context.executeRoiExtractorStrategy()

context.contourDetectorStrategy = BlurThresholdContourDetector(printer, roi)
contours = context.executeContourDetectorStrategy()


#context.contourFiltratorStrategy = FilterOnConditions(printer, contours)
#filtratedContours = context.executeContourFiltratorStrategy()

filtrator = FilterOnConditions(printer, contours)
filtratedContours = filtrator.touchEdgeFilter(contours, height, width)

context.contourSelectorStrategy = HierarchicalSelector(printer, filtratedContours)
selectedContour = context.executeContourSelectorStrategy()

averagor = ColorAveragor(printer, roi, selectedContour)
average = averagor.averageColor()

print(average)

cv.waitKey(0)

cv.destroyAllWindows()

