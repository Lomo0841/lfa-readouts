import numpy as np
import sys
import cv2 as cv
from lfa_project.Interfaces.IContourSelector import IContourSelector
import time as t

class HierarchicalSelector(IContourSelector):

    def __init__(self, printer, image, contours):
        self._printer = printer
        self._image = image
        self._contours = contours
        
    def select_contour(self):
        selected_contour = None

        if len(self._contours) == 0:            
            raise Exception("No contours to select from after deepsearch. Terminating program.")

        if len(self._contours) == 1:
            selected_contour = self._contours[0]
        else:
            selected_contour = self._select_outermost(self._contours)

        self._printer.write_image(self._image, "SelectedContour", selected_contour)

        return selected_contour

    def _select_outermost(self, contours):
        contour_areas = map(lambda cnt : cv.contourArea(cnt), contours)

        largest_contour = np.argmax(list(contour_areas))

        return contours[largest_contour]
