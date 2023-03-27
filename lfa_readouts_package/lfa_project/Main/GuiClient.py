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
    
        #Setting up instances
        self.context = Context()

        self.printer = Printer()

        self.input_image = input_image

        #THIS SHOULD BE OUTSOURCED TO THE TAKE PICTURE CLASS
        self.printer.write_image(self.input_image, "OriginalImage")

        self.config = ConfigReader()

    def findRoi(self):
        self.context.roiExtractorStrategy = AprilTagsExtractor(self.printer, self.input_image)
        roi = self.context.executeRoiExtractorStrategy()

        return roi

    def run_algorithm_on_roi(self, roi):

        self.context.contourDetectorStrategy = BlurThresholdContourDetector(self.printer, self.config ,roi.copy())
        contours = self.context.executeContourDetectorStrategy()

        self.context.contourFiltratorStrategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
        filtrated_contours = self.context.executeContourFiltratorStrategy()

        if len(filtrated_contours) == 0:
            self.context.contourDetectorStrategy = DeepSearch(self.printer, roi.copy())
            contours = self.context.executeContourDetectorStrategy()
            
            self.context.contourFiltratorStrategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
            filtrated_contours = self.context.executeContourFiltratorStrategy()

        self.context.contourSelectorStrategy = HierarchicalSelector(self.printer, roi.copy(), filtrated_contours)
        selected_contour = self.context.executeContourSelectorStrategy()

        averagor = ColorAveragor(self.printer, roi.copy(), selected_contour)

        avg_color = averagor.average_color()

        return (selected_contour, avg_color)
