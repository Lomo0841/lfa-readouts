from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor
from lfa_project.Implementations.Context import Context
from lfa_project.Implementations.DeepSearch import DeepSearch
from lfa_project.Utility.Printer import Printer
from lfa_project.Utility.ConfigReader import ConfigReader
from lfa_project.Implementations.GreyWorld import GreyWorld
from lfa_project.Implementations.MaxRGB import MaxRGB
from lfa_project.Implementations.AltContourDetector import AltContourDetector

class GuiWorkFlowClient():
        
    def __init__(self, input_image):
        self.context = Context()

        self.printer = Printer()

        self.input_image = input_image

        self.printer.write_image(self.input_image, "OriginalImage")

        self.config = ConfigReader()

    def findRoi(self):
        section = "Implementations"
        roi_extractor_choice = self.config.get_config_string(section, "iroiextractor")
        white_balancer_choice = self.config.get_config_string(section, "iwhitebalancer")

        if roi_extractor_choice == "AprilTagsExtractor":
            self.context.roiExtractorStrategy = AprilTagsExtractor(self.printer, self.input_image)
            roi = self.context.executeRoiExtractorStrategy()

        if white_balancer_choice == "GreyWorld":
            self.context.whiteBalancingStrategy = GreyWorld(self.printer, roi.copy())
            white_balanced = self.context.executeWhiteBalancingStrategy()
        elif white_balancer_choice == "MaxRGB":
            self.context.whiteBalancingStrategy = MaxRGB(self.printer, roi.copy())
            white_balanced = self.context.executeWhiteBalancingStrategy()

        return white_balanced

    def run_algorithm_on_roi(self, roi):
        section = "Implementations"
        contour_detector_choice = self.config.get_config_string(section, "icontourdetector")
        contour_filtrator_choice = self.config.get_config_string(section, "icontourfiltrator")
        contour_selector_choice = self.config.get_config_string(section, "icontourselector")

        if contour_detector_choice == "BlurThresholdContourDetector":
            self.context.contourDetectorStrategy = BlurThresholdContourDetector(self.printer, self.config, roi.copy())
            contours = self.context.executeContourDetectorStrategy()
        elif contour_detector_choice == "AltContourDetector":
            self.context.contourDetectorStrategy = AltContourDetector(self.printer, self.config, roi.copy())
            contours = self.context.executeContourDetectorStrategy()

        if contour_filtrator_choice == "FilterOnConditions":
            self.context.contourFiltratorStrategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
            filtrated_contours = self.context.executeContourFiltratorStrategy()

        if len(filtrated_contours) == 0:
            self.context.contourDetectorStrategy = DeepSearch(self.printer, roi.copy())
            contours = self.context.executeContourDetectorStrategy()
            
            self.context.contourFiltratorStrategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
            filtrated_contours = self.context.executeContourFiltratorStrategy()

        if contour_selector_choice == "HierarhicalSelector":
            self.context.contourSelectorStrategy = HierarchicalSelector(self.printer, roi.copy(), filtrated_contours)
            selected_contour = self.context.executeContourSelectorStrategy()

        averagor = ColorAveragor(self.printer, roi.copy(), selected_contour)
        avg_color = averagor.average_color()

        return (selected_contour, avg_color)
