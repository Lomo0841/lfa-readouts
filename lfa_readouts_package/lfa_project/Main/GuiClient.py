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

""" imageName = "green.png"

if platform.system() == 'Windows':
    inputImage = cv.imread("lfa_readouts_package\lfa_project\Images\\" + imageName)
else:
    inputImage = cv.imread("lfa_project/Images/" + imageName) """
class GuiClient():
        
    def __init__(self, inputImage):

    
        #Setting up instances
        self.context = Context()

        self.printer = Printing()


        self.inputImage = inputImage

        #THIS SHOULD BE OUTSOURCED TO THE TAKE PICTURE CLASS
        self.printer.write_image(self.inputImage, "OriginalImage")

    def findRoi(self):
        self.context.roiExtractorStrategy = AprilTagsExtractor(self.printer, self.inputImage)
        roi = self.context.executeRoiExtractorStrategy()

        return roi

    def runTheAlgorithmToFindTheContoursAndThenTheColorAndThenTheResult(self, roi):
        self.config = ConfigReader()

        self.context.contourDetectorStrategy = BlurThresholdContourDetector(self.printer, roi.copy())
        contours = self.context.executeContourDetectorStrategy()

        self.context.contourFiltratorStrategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
        filtratedContours = self.context.executeContourFiltratorStrategy()

        if len(filtratedContours) == 0:
            print("Entering Deep Search...")
            self.context.contourDetectorStrategy = DeepSearch(self.printer, roi.copy())
            contours = self.context.executeContourDetectorStrategy()
            
            self.context.contourFiltratorStrategy = FilterOnConditions(self.printer, self.config, roi.copy(), contours)
            filtratedContours = self.context.executeContourFiltratorStrategy()

        self.context.contourSelectorStrategy = HierarchicalSelector(self.printer, roi.copy(), filtratedContours)
        selectedContour = self.context.executeContourSelectorStrategy()

        averagor = ColorAveragor(self.printer, roi.copy(), selectedContour)

        averagor.averageColor()

#cv.waitKey(0)

#cv.destroyAllWindows()
