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

class GuiClient():
        
    def __init__(self, input_image):
        self.context = Context()

        self.config = ConfigReader()

        self.printer = Printer(self.config)

        self.input_image = input_image

        self.printer.write_image(self.input_image, "OriginalImage")

    def find_roi(self):
        section = "Implementations"
        roi_extractor_choice = self.config.get_config_string(section, "iroiextractor")
        white_balancer_choice = self.config.get_config_string(section, "iwhitebalancer")

        if roi_extractor_choice == "AprilTagsExtractor":
            self.context.roi_extractor_strategy = AprilTagsExtractor(self.printer, self.input_image)
            roi = self.context.execute_roi_extractor_strategy()

        if white_balancer_choice == "GreyWorld":
            self.context.white_balancing_strategy = GreyWorld(self.printer, roi.copy())
            white_balanced = self.context.execute_white_balancing_strategy()
        elif white_balancer_choice == "MaxRGB":
            self.context.white_balancing_strategy = MaxRGB(self.printer, roi.copy())
            white_balanced = self.context.execute_white_balancing_strategy()
        elif white_balancer_choice == "None":
            white_balanced = roi

        return white_balanced

    def run_algorithm_on_roi(self, roi):
        config = ConfigReader()

        section = "Implementations"
        contour_detector_choice = self.config.get_config_string(section, "icontourdetector")
        contour_filtrator_choice = self.config.get_config_string(section, "icontourfiltrator")
        contour_selector_choice = self.config.get_config_string(section, "icontourselector")

        if contour_detector_choice == "BlurThresholdContourDetector":
            self.context.contour_detector_strategy = BlurThresholdContourDetector(self.printer, config, roi.copy())
            contours = self.context.execute_contour_detector_strategy()
        elif contour_detector_choice == "AltContourDetector":
            self.context.contour_detector_strategy = AltContourDetector(self.printer, config, roi.copy())
            contours = self.context.execute_contour_detector_strategy()

        if contour_filtrator_choice == "FilterOnConditions":
            self.context.contour_filtrator_strategy = FilterOnConditions(self.printer, config, roi.copy(), contours)
            filtrated_contours = self.context.execute_contour_filtrator_strategy()

        if len(filtrated_contours) == 0:
            self.context.contour_detector_strategy = DeepSearch(self.printer, roi.copy())
            contours = self.context.execute_contour_detector_strategy()
            
            self.context.contour_filtrator_strategy = FilterOnConditions(self.printer, config, roi.copy(), contours)
            filtrated_contours = self.context.execute_contour_filtrator_strategy()

        if contour_selector_choice == "HierarchicalSelector":
            self.context.contour_selector_strategy = HierarchicalSelector(self.printer, roi.copy(), filtrated_contours)
            selected_contour = self.context.execute_contour_selector_strategy()

        averagor = ColorAveragor(self.printer, roi.copy(), selected_contour)
        avg_color = averagor.average_color()

        return (selected_contour, avg_color)
