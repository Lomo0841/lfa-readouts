import numpy as np
import sys
import cv2 as cv
from lfa_project.Interfaces.IContourSelector import IContourSelector
import time as t

class HierarchicalSelector(IContourSelector):

    def __init__(self, printer, image, contours):
        self.printer = printer
        self.image = image
        self.contours = contours
        
    def selectContour(self):
        selectedContour = None

        if len(self.contours) == 0:
            #print("No contours to select from after deepsearch. Terminating program.")
            sys.exit(1)
        if len(self.contours) == 1:
            selectedContour = self.contours[0]
        else:
            selectedContour = self.selectOutermost(self.contours)

        self.printer.write_image(self.image, "SelectedContour", selectedContour)

        return selectedContour

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
