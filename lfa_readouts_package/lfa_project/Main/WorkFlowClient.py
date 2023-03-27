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
from lfa_project.Implementations.GreyWorld import GreyWorld
from lfa_project.Implementations.MaxRGB import MaxRGB
from lfa_project.Utility.Printer import Printer
from lfa_project.Utility.ConfigReader import ConfigReader

image_name = "green.png"

if platform.system() == 'Windows':
    input_image = cv.imread("lfa_readouts_package\lfa_project\Images\TwoLeds\\" + image_name)
else:
    input_image = cv.imread("lfa_readouts_package/lfa_project/Images/TwoLeds/" + image_name)

#Setting up
context = Context()

printer = Printer()

config = ConfigReader()

printer.write_image(input_image, "OriginalImage")

section = "Implementations"
roi_extractor_choice = config.get_config_string(section, "iroiextractor")
white_balancer_choice = config.get_config_string(section, "iwhitebalancer")
contour_detector_choice = config.get_config_string(section, "icontourdetector")
contour_filtrator_choice = config.get_config_string(section, "icontourfiltrator")
contour_selector_choice = config.get_config_string(section, "icontourselector")

if roi_extractor_choice == "AprilTagsExtractor":
    context.roiExtractorStrategy = AprilTagsExtractor(printer, input_image)
    roi = context.executeRoiExtractorStrategy()
    print("april")

if white_balancer_choice == "GreyWorld":
    context.whiteBalancingStrategy = GreyWorld(printer, roi.copy())
    white_balanced = context.executeWhiteBalancingStrategy()
    print("grey")
elif white_balancer_choice == "MaxRGB":
     context.whiteBalancingStrategy = MaxRGB(printer, roi.copy())
     white_balanced = context.executeWhiteBalancingStrategy()
     print("Max")

if contour_detector_choice == "BlurThresholdContourDetector":
    context.contourDetectorStrategy = BlurThresholdContourDetector(printer, config, white_balanced.copy())
    contours = context.executeContourDetectorStrategy()
    print("blurthreshold")
elif contour_detector_choice == "AltContourDetector":
    context.contourDetectorStrategy = AltContourDetector(printer, config, white_balanced.copy())
    contours = context.executeContourDetectorStrategy()
    print("alt")

if contour_filtrator_choice == "FilterOnConditions":
    context.contourFiltratorStrategy = FilterOnConditions(printer, config, white_balanced.copy(), contours)
    filtratedContours = context.executeContourFiltratorStrategy()
    print("conditions")

if len(filtratedContours) == 0:
    context.contourDetectorStrategy = DeepSearch(printer, white_balanced.copy())
    contours = context.executeContourDetectorStrategy()
    print("deep")

    context.contourFiltratorStrategy = FilterOnConditions(printer, config, white_balanced.copy(), contours)
    filtratedContours = context.executeContourFiltratorStrategy()

if contour_selector_choice == "HierarhicalSelector":
    context.contourSelectorStrategy = HierarchicalSelector(printer, white_balanced.copy(), filtratedContours)
    selectedContour = context.executeContourSelectorStrategy()
    print("hierarchical")

averagor = ColorAveragor(printer, roi.copy(), selectedContour)
averagor.average_color()

print("You made it to the final statement.")
