import numpy as np
import sys
import cv2 as cv
from lfa_project.Interfaces.IContourSelector import IContourSelector
import time as t

class HierarchicalSelector(IContourSelector):

    def __init__(self, printer):
        self.printer = printer
        
    def selectContour(self, contours) -> np.ndarray:
        if len(contours) == 0:
            sys.exit(1)
        if len(contours) == 1:
            return contours[0]
        else:
            return self.selectOutermost(contours)

    def selectOutermost(self, contours):
        """ largest_contour = None
        largest_area = 0
        for contour in contours:
            area = cv.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_contour = contour
      
        return largest_contour """
    
        contourAreas = map(lambda cnt : cv.contourArea(cnt), contours)

        largestContour = np.argmax(list(contourAreas))

        return contours[largestContour]
