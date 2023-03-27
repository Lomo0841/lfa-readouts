import cv2 as cv
import platform 
from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.AltContourDetector import AltContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor
from lfa_project.Implementations.Context import Context
from lfa_project.Implementations.DeepSearch import DeepSearch
from lfa_project.Utility.Printer import Printer
from lfa_project.Utility.ConfigReader import ConfigReader

image_name = "blurryorange.png"

if platform.system() == 'Windows':
    input_image = cv.imread("lfa_readouts_package\lfa_project\Images\TwoLeds\\" + image_name)
else:
    input_image = cv.imread("lfa_readouts_package/lfa_project/Images/TwoLeds/" + image_name)


#Setting up instances
context = Context()

printer = Printer()

config = ConfigReader()

#THIS SHOULD BE OUTSOURCED TO THE TAKE PICTURE CLASS
printer.write_image(input_image, "OriginalImage")

context.roiExtractorStrategy = AprilTagsExtractor(printer, input_image)
roi = context.executeRoiExtractorStrategy()

context.contourDetectorStrategy = BlurThresholdContourDetector(printer, config, roi.copy())
#context.contourDetectorStrategy = AltContourDetector(printer, config, roi.copy())
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
averagor.average_color()

print("You made it to the final statement.")

#cv.waitKey(0)

#cv.destroyAllWindows()
