import cv2 as cv
import numpy as np
import itertools
from lfa_project.Interfaces.IContourDetector import IContourDetector

class DeepSearch(IContourDetector):

    def __init__(self, printer, image):
        self.printer = printer
        self.image = image

    def detectContours(self):
        min, max = self.analyseHistogram(self.image)

        allContours = self.runAllContours(min, max, self.image)

        return allContours

    def analyseHistogram(self, image):
        grayScale = self.greyScale(image)

        histogram = cv.calcHist([grayScale], [0], None, [256], [0, 256])

        indices = np.nonzero(histogram)[0]

        minIndex = indices.min()

        maxIndex = indices.max()

        return minIndex, maxIndex

    def runAllContours(self, min, max, image):

        allContours= []

        blur = cv.GaussianBlur(image, (5, 5), 0)

        greyScale = self.greyScale(blur)

        for i in range(min, max):
            ret, thresholdedImage = cv.threshold(greyScale, i, 255, cv.THRESH_BINARY)

            contours, hierarchy = cv.findContours(thresholdedImage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            allContours.append(contours)


        flatContours = list(itertools.chain(*allContours))

        return flatContours

    def greyScale(self, image):
        
        greyScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        return greyScale
              