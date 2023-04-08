import cv2 as cv
import numpy as np
import math
from lfa_project.Interfaces.IContourFiltrator import IContourFiltrator

class FilterOnConditions(IContourFiltrator):

    def __init__(self, printer, config, image, contours):
        self._printer = printer
        self._image = image
        self._contours = contours
        self._config = config
    
    def filter_contours(self):
        section = "FiltrationVariables"
        min_area = self._config.get_config_int(section, "minAreaOfContour")
        max_depth = self._config.get_config_int(section, "maxDepthOfConvex")
        expected_centrum_x = self._config.get_config_int(section, "expectedCentrumX")
        expected_centrum_y = self._config.get_config_int(section, "expectedCentrumY")
        max_distance_from_centrum = self._config.get_config_int(section, "maxDistanceFromCentrum")

        area_filtered = self._area_filter(self._contours, min_area)

        touch_edge_filtered = self._touch_edge_filter(area_filtered)

        convexity_defect_filtered = self._convexity_defect_filter(touch_edge_filtered, max_depth)

        centroid_distance_filtered = self._centroid_distance_filter(convexity_defect_filtered, expected_centrum_x, expected_centrum_y, max_distance_from_centrum)

        #Do we need this?
        #pointFiltered = self.pointFilter(convexityDefectFiltered, points)

        self._printer.write_image(self._image, "FilteredContours", centroid_distance_filtered)

        return centroid_distance_filtered

    def _point_filter(self, contours, points):
        filtered_contours = []
        for cnt in contours:
            if all(cv.pointPolygonTest(cnt, p, measureDist=False) >= 0 for p in points):
                filtered_contours.append(cnt)
        return filtered_contours

    def _area_filter(self, contours, min_area):
        filtered_contours = []
        
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > min_area:
                filtered_contours.append(cnt)
            
        return filtered_contours

    def _touch_edge_filter(self, contours):
        filtered_contours = []

        height, width = self._image.shape[:2]

        for cnt in contours:
            x = cnt[:, 0][:, 0]
            y = cnt[:, 0][:, 1]

            max_x = x[np.argmax(x)]
            min_x = x[np.argmin(x)]
            max_y = y[np.argmax(y)]
            min_y = y[np.argmin(y)]

            if min_x > 0 and max_x < width and min_y > 0 and max_y < height:
                filtered_contours.append(cnt)

        return filtered_contours

    def _convexity_defect_filter(self, contours, max_depth):
        filtered_contours = []

        for cnt in contours:
            hull = cv.convexHull(cnt, returnPoints=False)
            
            try:
                self._defect_check(max_depth, filtered_contours, cnt, hull)
            except:
                hull[::-1].sort(axis=0)
                self._defect_check(max_depth, filtered_contours, cnt, hull)

        return filtered_contours

    def _defect_check(self, max_depth, filtered_contours, cnt, hull):
        defects = cv.convexityDefects(cnt, hull)

        if defects is not None and len(defects) > 0:
            max_defect = np.max(defects[:, 0, 3])/256

            if max_defect <= max_depth:
                filtered_contours.append(cnt)
        else:
            filtered_contours.append(cnt)

    
    def _centroid_distance_filter(self, contours, expected_centrum_x, expected_centrum_y, max_distance_from_centrum):
        filtered_contours = []
        c_x = 0 
        c_y = 0

        for cnt in contours: 
            m = cv.moments(cnt)
        

            if m['m00'] != 0:
                c_x = int(m['m10']/m['m00'])
                c_y = int(m['m01']/m['m00'])

            distance = math.sqrt((c_x - expected_centrum_x)**2 + (c_y - expected_centrum_y)**2)
            
            if distance <= max_distance_from_centrum:
                filtered_contours.append(cnt)
       
        return filtered_contours
