from lfa_project.Implementations.AprilTagsExtractor import AprilTagsExtractor
from lfa_project.Implementations.BlurThresholdContourDetector import BlurThresholdContourDetector
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector
from lfa_project.Implementations.ColorAveragor import ColorAveragor
from lfa_project.Implementations.Context import Context
from lfa_project.Implementations.DeepSearch import DeepSearch
from lfa_project.Utility.Printer import Printer
from lfa_project.Utility.ConfigReader import ConfigReader

class GuiClient():
        
    def __init__(self, input_image):
    
        # Setting up instances
        self.context = Context()
        self.printer = Printer()
        self.input_image = input_image

        # THIS SHOULD BE OUTSOURCED TO THE TAKE PICTURE CLASS
        self.printer.write_image(self.input_image, "original_image")

    def find_roi(self):
        self.context.roi_extractor_strategy = AprilTagsExtractor(self.printer, self.input_image)
        roi = self.context.execute_roi_extractor_strategy()

        return roi

    def run_algorithm_on_roi(self, roi):

        self.context.contour_detector_strategy = BlurThresholdContourDetector(self.printer, self.config ,roi.copy())
        contours = self.context.execute_contour_detector_strategy()

        self.context.contour_filtrator_strategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
        filtered_contours = self.context.execute_contour_filtrator_strategy()

        if len(filtered_contours) == 0:
            self.context.contour_detector_strategy = DeepSearch(self.printer, roi.copy())
            contours = self.context.execute_contour_detector_strategy()
            
            self.context.contour_filtrator_strategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
            filtered_contours = self.context.execute_contour_filtrator_strategy()

        self.context.contour_selector_strategy = HierarchicalSelector(self.printer, roi.copy(), filtered_contours)
        selected_contour = self.context.execute_contour_selector_strategy()

        averagor = ColorAveragor(self.printer, roi.copy(), selected_contour)

        avg_color = averagor.average_color()

        return (selected_contour, avg_color)
