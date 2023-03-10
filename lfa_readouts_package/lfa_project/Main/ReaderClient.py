import cv2 as cv
import time as t
import platform 
from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor
from lfa_project.Implementations.Context import Context
from lfa_project.Implementations.DeepSearch import DeepSearch
from lfa_project.Utility.Printing import Printing
from lfa_project.Utility.ConfigReader import ConfigReader

imageName = "green.png"

if platform.system() == 'Windows':
    inputImage = cv.imread("lfa_readouts_package\lfa_project\Images\\" + imageName)
else:
    inputImage = cv.imread("lfa_project/Images/" + imageName)


#Setting up instances
context = Context()

printer = Printing()

config = ConfigReader()

#THIS SHOULD BE OUTSOURCED TO THE TAKE PICTURE CLASS
printer.write_image(inputImage, "OriginalImage")

start = t.time()
context.roiExtractorStrategy = AprilTagsExtractor(printer, inputImage)
roi = context.executeRoiExtractorStrategy()
print(t.time()-start)

context.contourDetectorStrategy = BlurThresholdContourDetector(printer, roi.copy())
contours = context.executeContourDetectorStrategy()

context.contourFiltratorStrategy = FilterOnConditions(printer, config, roi.copy(), contours)
filtratedContours = context.executeContourFiltratorStrategy()

if len(filtratedContours) == 0:
    context.contourDetectorStrategy = DeepSearch(printer, roi.copy())
    contours = context.executeContourDetectorStrategy()
    
    context.contourFiltratorStrategy = FilterOnConditions(printer, config, roi.copy(), contours)
    filtratedContours = context.executeContourFiltratorStrategy()

context.contourSelectorStrategy = HierarchicalSelector(printer, roi.copy(), filtratedContours)
selectedContour = context.executeContourSelectorStrategy()

averagor = ColorAveragor(printer, roi.copy(), selectedContour)

averagor.averageColor()

#cv.waitKey(0)

#cv.destroyAllWindows()
