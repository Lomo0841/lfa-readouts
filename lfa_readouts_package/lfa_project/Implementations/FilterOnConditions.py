import cv2 as cv
import numpy as np
import math
from lfa_project.Interfaces.IContourFiltrator import IContourFiltrator

#THE RETURN TYPE SHOULD BE CHANGE TO RETURN A LIST OF COUNTOURS

#maybe every parameter in the constructor should be given as fields gotten from a config file
class FilterOnConditions(IContourFiltrator):
    
    def filterContours(self, contours, minArea, height, width, maxdepth, points) -> np.ndarray:

        areafilterered = self.areaFilter(contours, minArea)

        touchEdgeFiltered = self.touchEdgeFilter(areafilterered, height, width)

        convexityDetectFiltered = self.convexityDetectFilter(touchEdgeFiltered, maxdepth)

        pointFiltered = self.pointFilter(convexityDetectFiltered, points)

        return pointFiltered

    #Where does it recieve the points from? 
    def pointFilter(self, contours, points) -> np.ndarray:
        filteredContours = []
        for cnt in contours:
            if all(cv.pointPolygonTest(cnt, p, measureDist=False) >= 0 for p in points):
                filteredContours.append(cnt)
        return filteredContours

    

    def areaFilter(self, contours, minArea) -> np.ndarray:
        #Iterate over the contours and filter them based on area
        filteredContours = []
        
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > minArea:
                filteredContours.append(cnt)
            
        return filteredContours

    #Maybe use numpy and argmax (and big if statement?)
    def touchEdgeFilter(self, contours, height, width) -> np.ndarray:
        filteredContours = []

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

    def convexityDetectFilter(self, contours, maxDepth) -> np.ndarray:
        #Iterate over the contours and filter them based on area
        filteredContours = []

        for cnt in contours:
            hull = cv.convexHull(cnt, returnPoints=False)
            defects = cv.convexityDefects(cnt, hull)

            if defects is not None and len(defects) > 0:
                maxDefect = np.max(defects[:, 0, 3])

                if maxDefect <= maxDepth:
                    filteredContours.append(cnt)

            else:

                filteredContours.append(cnt)

        return filteredContours
    
    def centroidDistanceFilter(self, contours, expectedCentrumX, expectedCentrumY, maxDistanceToCentrum) -> np.ndarray:
        filteredContours = []
        cx = 0 
        cy = 0

        for cnt in contours: 
            m = cv.moments(cnt)
        

            if m['m00'] != 0:
                cx = int(m['m10']/m['m00'])
                cy = int(m['m01']/m['m00'])

            distance = math.sqrt((cx - expectedCentrumX)**2 + (cy - expectedCentrumY)**2)
            
            if distance <= maxDistanceToCentrum:
                filteredContours.append(cnt)
       
        return filteredContours


            

            

            





        
        
