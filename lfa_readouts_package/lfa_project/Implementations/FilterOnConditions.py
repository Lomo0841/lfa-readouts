import cv2 as cv
import numpy as np
import math
from lfa_project.Interfaces.IContourFiltrator import IContourFiltrator

class FilterOnConditions(IContourFiltrator):

    def __init__(self, printer, config, image, contours):
        self.printer = printer
        self.image = image
        self.contours = contours
        self.config = config
    
    def filterContours(self):
        section = "FiltrationVariables"
        minArea = self.config.getConfigInt(section, "minAreaOfContour")
        maxDepth = self.config.getConfigInt(section, "maxDepthOfConvex")
        expectedCentrumX = self.config.getConfigInt(section, "expectedCentrumX")
        expectedCentrumY = self.config.getConfigInt(section, "expectedCentrumY")
        maxDistanceFromCentrum = self.config.getConfigInt(section, "maxDistanceFromCentrum")

        areaFiltered = self.areaFilter(self.contours, minArea)

        touchEdgeFiltered = self.touchEdgeFilter(areaFiltered)

        convexityDefectFiltered = self.convexityDefectFilter(touchEdgeFiltered, maxDepth)

        centroidDistanceFiltered = self.centroidDistanceFilter(convexityDefectFiltered, expectedCentrumX, expectedCentrumY, maxDistanceFromCentrum)

        #Do we need this?
        #pointFiltered = self.pointFilter(convexityDefectFiltered, points)

        self.printer.write_image(self.image, "FilteredContours", centroidDistanceFiltered)

        return centroidDistanceFiltered

    #Where does it recieve the points from? 
    def pointFilter(self, contours, points):
        filteredContours = []
        for cnt in contours:
            if all(cv.pointPolygonTest(cnt, p, measureDist=False) >= 0 for p in points):
                filteredContours.append(cnt)
        return filteredContours

    

    def areaFilter(self, contours, minArea):
        filteredContours = []
        
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > minArea:
                filteredContours.append(cnt)
            
        return filteredContours

    def touchEdgeFilter(self, contours):
        filteredContours = []

        height, width = self.image.shape[:2]

        for cnt in contours:
            x = cnt[:, 0][:, 0]
            y = cnt[:, 0][:, 1]

            maxX = x[np.argmax(x)]
            minX = x[np.argmin(x)]
            maxY = y[np.argmax(y)]
            minY = y[np.argmin(y)]

            if minX > 0 and maxX < width and minY > 0 and maxY < height:
                filteredContours.append(cnt)

        return filteredContours

    def convexityDefectFilter(self, contours, maxDepth):
            
        filteredContours = []

        for cnt in contours:
            hull = cv.convexHull(cnt, returnPoints=False)

            try:
                self.defectCheck(maxDepth, filteredContours, cnt, hull)
            except:
                hull[::-1].sort(axis=0)
                self.defectCheck(maxDepth, filteredContours, cnt, hull)

        return filteredContours

    def defectCheck(self, maxDepth, filteredContours, cnt, hull):
        defects = cv.convexityDefects(cnt, hull)

        if defects is not None and len(defects) > 0:
            maxDefect = np.max(defects[:, 0, 3])

            if maxDefect <= maxDepth:
                filteredContours.append(cnt)
        else:
            filteredContours.append(cnt)

    
    def centroidDistanceFilter(self, contours, expectedCentrumX, expectedCentrumY, maxDistanceFromCentrum):
        filteredContours = []
        cx = 0 
        cy = 0

        for cnt in contours: 
            m = cv.moments(cnt)
        

            if m['m00'] != 0:
                cx = int(m['m10']/m['m00'])
                cy = int(m['m01']/m['m00'])

            distance = math.sqrt((cx - expectedCentrumX)**2 + (cy - expectedCentrumY)**2)
            
            if distance <= maxDistanceFromCentrum:
                filteredContours.append(cnt)
       
        return filteredContours
    

"""         filteredContours = []

        for cnt in contours:
            hull = cv.convexHull(cnt, returnPoints=False)
            defects = cv.convexityDefects(cnt, hull)

            if defects is not None and len(defects) > 0:
                maxDefect = np.max(defects[:, 0, 3])

                if maxDefect <= maxDepth:
                    filteredContours.append(cnt)

            else:

                filteredContours.append(cnt)

        return filteredContours """


""" for cnt in contours:
            x = cnt[:, 0][:, 0]
            y = cnt[:, 0][:, 1]
            flag = False
        
            for value in x:
                if value <= 0 or value >= width: 
                    flag = True
                    break
                
            if flag:
                continue

            for value in y:
                if value <= 0 or value >= height:
                    flag = True
                    break
                
            if flag:
                continue
    
            filteredContours.append(cnt) """
