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

image_name = "orange_dot.png"

if platform.system() == 'Windows':
    input_image = cv.imread("lfa_readouts_package\lfa_project\Images\memory_and_time_samples\\" + image_name)
else:
    input_image = cv.imread("lfa_readouts_package/lfa_project/Images/memory_and_time_samples/" + image_name)

context = Context()

config = ConfigReader()

printer = Printer(config)

printer.write_image(input_image, "OriginalImage")

section = "Implementations"
roi_extractor_choice = config.get_config_string(section, "iroiextractor")
white_balancer_choice = config.get_config_string(section, "iwhitebalancer")
contour_detector_choice = config.get_config_string(section, "icontourdetector")
contour_filtrator_choice = config.get_config_string(section, "icontourfiltrator")
contour_selector_choice = config.get_config_string(section, "icontourselector")

if roi_extractor_choice == "AprilTagsExtractor":
    context.roi_extractor_strategy = AprilTagsExtractor(printer, input_image)
    roi = context.execute_roi_extractor_strategy()

if white_balancer_choice == "GreyWorld":
    context.white_balancing_strategy = GreyWorld(printer, roi.copy())
    white_balanced = context.execute_white_balancing_strategy()
elif white_balancer_choice == "MaxRGB":
     context.white_balancing_strategy = MaxRGB(printer, roi.copy())
     white_balanced = context.execute_white_balancing_strategy()
elif white_balancer_choice == "None":
    white_balanced = roi

if contour_detector_choice == "BlurThresholdContourDetector":
    context.contour_detector_strategy = BlurThresholdContourDetector(printer, config, white_balanced.copy())
    contours = context.execute_contour_detector_strategy()
elif contour_detector_choice == "AltContourDetector":
    context.contour_detector_strategy = AltContourDetector(printer, config, white_balanced.copy())
    contours = context.execute_contour_detector_strategy()

if contour_filtrator_choice == "FilterOnConditions":
    context.contour_filtrator_strategy = FilterOnConditions(printer, config, white_balanced.copy(), contours)
    filtrated_contours = context.execute_contour_filtrator_strategy()

if len(filtrated_contours) == 0:
    context.contour_detector_strategy = DeepSearch(printer, white_balanced.copy())
    contours = context.execute_contour_detector_strategy()

    context.contour_filtrator_strategy = FilterOnConditions(printer, config, white_balanced.copy(), contours)
    filtrated_contours = context.execute_contour_filtrator_strategy()

if contour_selector_choice == "HierarchicalSelector":
    context.contour_selector_strategy = HierarchicalSelector(printer, white_balanced.copy(), filtrated_contours)
    selected_contour = context.execute_contour_selector_strategy()

averagor = ColorAveragor(printer, white_balanced.copy(), selected_contour)
averagor.average_color()
