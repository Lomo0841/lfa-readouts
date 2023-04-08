import cv2 as cv
import time as t
import platform 
from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor
from lfa_project.Utility.Printer import Printing
from lfa_project.Implementations.Context import Context

cam = cv.VideoCapture(0)

ret, inputImage = cam.read()

cam.release()

height, width = inputImage.shape[:2]

#Setting up instances
context = Context()

_printer = Printing()

start = t.time()
#THIS SHOULD BE OUTSOURCED TO THE TAKE PICTURE CLASS
_printer.write_image(inputImage, "OriginalImage")

context.roiExtractorStrategy = AprilTagsExtractor(_printer, inputImage)
roi = context.executeRoiExtractorStrategy()

context.contourDetectorStrategy = BlurThresholdContourDetector(_printer, roi.copy())
_contours = context.executeContourDetectorStrategy()

#context.contourFiltratorStrategy = FilterOnConditions(printer, contours)
#filtratedContours = context.executeContourFiltratorStrategy()

filtrator = FilterOnConditions(_printer, roi.copy(), _contours)
filtratedContours = filtrator._touch_edge_filter(_contours, height, width)

context.contourSelectorStrategy = HierarchicalSelector(_printer, roi.copy(), filtratedContours)
selectedContour = context.executeContourSelectorStrategy()

averagor = ColorAveragor(_printer, roi.copy(), selectedContour)
averagor.average_color()

print(t.time()-start)
#cv.waitKey(0)

#cv.destroyAllWindows()
