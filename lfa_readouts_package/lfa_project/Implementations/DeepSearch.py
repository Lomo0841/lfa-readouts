import cv2 as cv
import numpy as np
import itertools
from lfa_project.Interfaces.IContourDetector import IContourDetector

class DeepSearch(IContourDetector):

    def __init__(self, printer, image):
        self.printer = printer
        self.image = image

    def detect_contours(self):
        min, max = self.analyse_histogram(self.image)

        all_contours = self.run_all_contours(min, max, self.image)

        return all_contours

    def analyse_histogram(self, image):
        gray_scale = self.grey_scale(image)

        histogram = cv.calcHist([gray_scale], [0], None, [256], [0, 256])

        indices = np.nonzero(histogram)[0]

        min_index = indices.min()

        max_index = indices.max()

        return min_index, max_index

    def run_all_contours(self, min, max, image):

        all_contours= []

        blur = cv.GaussianBlur(image, (5, 5), 0)

        grey_scale = self.grey_scale(blur)

        for i in range(min, max):
            _, thresholded_image = cv.threshold(grey_scale, i, 255, cv.THRESH_BINARY)

            contours, _ = cv.findContours(thresholded_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            all_contours.append(contours)


        flat_contours = list(itertools.chain(*all_contours))

        return flat_contours

    def grey_scale(self, image):
        
        grey_scale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        return grey_scale
              