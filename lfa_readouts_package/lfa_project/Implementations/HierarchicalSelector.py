import numpy as np
import sys
import cv2 as cv
from lfa_project.Interfaces.IContourSelector import IContourSelector

class HierarchicalSelector(IContourSelector):
        
    def selectContour(self, contours) -> np.ndarray:
        if len(contours) == 0:
            sys.exit(1)
        if len(contours) == 1:
            return contours[0]
        else:
            self.selectOutermost(contours)

    def selectOutermost(self, contours):
        contourAreas = map(lambda cnt : cv.contourArea(cnt), contours)
        largestContour = np.argmax(contourAreas)
        return contours[largestContour]

