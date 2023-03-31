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
import time as t

class GuiWorkFlowClient():
        
    def __init__(self, input_image):
        self.context = Context()

        self.config = ConfigReader()

        self.printer = Printer(self.config)

        self.input_image = input_image

        self.printer.write_image(self.input_image, "OriginalImage")


    def find_roi(self):

        total_start = t.time()

        roi_start = t.time()

        section = "Implementations"
        roi_extractor_choice = self.config.get_config_string(section, "iroiextractor")
        white_balancer_choice = self.config.get_config_string(section, "iwhitebalancer")

        if roi_extractor_choice == "AprilTagsExtractor":
            self.context.roi_extractor_strategy = AprilTagsExtractor(self.printer, self.input_image)
            roi = self.context.execute_roi_extractor_strategy()

        roi_end = t.time()

        self.printer.write_file("Roi detection: " + str(roi_end - roi_start))

        white_start = t.time()

        if white_balancer_choice == "GreyWorld":
            self.context.white_balancing_strategy = GreyWorld(self.printer, roi.copy())
            white_balanced = self.context.execute_white_balancing_strategy()
        elif white_balancer_choice == "MaxRGB":
            self.context.white_balancing_strategy = MaxRGB(self.printer, roi.copy())
            white_balanced = self.context.execute_white_balancing_strategy()
        elif white_balancer_choice == "None":
            white_balanced = roi

        white_end = t.time()

        self.printer.write_file("White balancing: " + str(white_end - white_start))

        total_end = t.time()

        self.printer.write_file("Total time 1: " + str(total_end - total_start))

        return white_balanced

    def run_algorithm_on_roi(self, roi):
        config = ConfigReader()

        total_start = t.time()

        section = "Implementations"
        contour_detector_choice = self.config.get_config_string(section, "icontourdetector")
        contour_filtrator_choice = self.config.get_config_string(section, "icontourfiltrator")
        contour_selector_choice = self.config.get_config_string(section, "icontourselector")

        contour_detect_start = t.time()

        if contour_detector_choice == "BlurThresholdContourDetector":
            self.context.contour_detector_strategy = BlurThresholdContourDetector(self.printer, config, roi.copy())
            contours = self.context.execute_contour_detector_strategy()
        elif contour_detector_choice == "AltContourDetector":
            self.context.contour_detector_strategy = AltContourDetector(self.printer, config, roi.copy())
            contours = self.context.execute_contour_detector_strategy()
        
        contour_detect_end = t.time()

        self.printer.write_file("Contour detection: " + str(contour_detect_end - contour_detect_start))

        contour_filtrate_start = t.time()

        if contour_filtrator_choice == "FilterOnConditions":
            self.context.contour_filtrator_strategy = FilterOnConditions(self.printer, config, roi.copy(), contours)
            filtrated_contours = self.context.execute_contour_filtrator_strategy()

        contour_filtrate_end = t.time()

        self.printer.write_file("Contour filtration: " + str(contour_filtrate_end - contour_filtrate_start))

        if len(filtrated_contours) == 0:

            deep_search_start = t.time()

            self.context.contour_detector_strategy = DeepSearch(self.printer, roi.copy())
            contours = self.context.execute_contour_detector_strategy()

            deep_search_end = t.time()

            self.printer.write_file("Deep search: " + str(deep_search_end - deep_search_start))

            contour_filtrate_start = t.time()
            
            self.context.contour_filtrator_strategy = FilterOnConditions(self.printer, config, roi.copy(), contours)
            filtrated_contours = self.context.execute_contour_filtrator_strategy()

            contour_filtrate_end = t.time()

            self.printer.write_file("Contour filtration: " + str(contour_filtrate_end - contour_filtrate_start))

        contour_selection_start = t.time()

        if contour_selector_choice == "HierarchicalSelector":
            self.context.contour_selector_strategy = HierarchicalSelector(self.printer, roi.copy(), filtrated_contours)
            selected_contour = self.context.execute_contour_selector_strategy()

        contour_selection_end = t.time()

        self.printer.write_file("Contour selection: " + str(contour_selection_end - contour_selection_start))

        average_start = t.time()

        averagor = ColorAveragor(self.printer, roi.copy(), selected_contour)
        avg_color = averagor.average_color()

        average_end = t.time()

        self.printer.write_file("Color average: " + str(average_end - average_start))

        total_end = t.time()

        self.printer.write_file("Total time 2: " + str(total_end - total_start))

        return (selected_contour, avg_color)
