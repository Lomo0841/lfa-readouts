import unittest
from unittest.mock import MagicMock
import numpy as np
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions
from lfa_project.Utility.ConfigReader import ConfigReader

class FilterOnConditionsTest(unittest.TestCase):

    def setUp(self):
        #Arrange
        self.printer = MagicMock()
        self.config = MagicMock()
        self.image = np.zeros((100,100), np.uint8)

    def testAreaFilter(self):
        #Arrange
        contourOver50 = np.array([[50,50], [100,50], [100,100], [50,100]])
        contourUnder50 = np.array([[1,1], [1,2], [2,1], [2,2]])

        contours = [contourOver50, contourUnder50]

        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)

        #Act
        areaFiltered = filtrator.areaFilter(contours, 50)
        areaFilteredList = [contour.tolist() for contour in areaFiltered]

        #Assert
        self.assertEqual(areaFilteredList, [contourOver50.tolist()])

    def testConvexityDefectFilter(self):
        #Arrange
        contourWithConvexityDefect = np.array([[0,0], [100,0], [50,50], [100,100], [0,100]])
        contourWithoutConvexityDefect = np.array([[200,200], [250,200], [250,250], [200,250]])
        contours = [contourWithConvexityDefect, contourWithoutConvexityDefect]
        maxDepth = 50
        
        #Act
        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)
        convexityDefectFiltered = filtrator.convexityDefectFilter(contours, maxDepth)
        convexityDefectFilteredList = [contour.tolist() for contour in convexityDefectFiltered]

        #Assert
        self.assertEqual(convexityDefectFilteredList, [contourWithoutConvexityDefect.tolist()])


    def testCentroidDistanceFilter(self):
        # Arrange
        expectedCentrumX = 50
        expectedCentrumY = 50
        maxDistanceFromCentrum = 10
        
        contourCenter5050 = np.array([[40, 40], [60, 40], [60, 60], [40, 60]])
        contourCenter2525 = np.array([[20, 20], [30, 20], [30, 30], [20, 30]])
        contours = [contourCenter5050, contourCenter2525]
        
        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)
        
        # Act
        centroidDistanceFiltered = filtrator.centroidDistanceFilter(contours, expectedCentrumX, expectedCentrumY, maxDistanceFromCentrum)
        centroidDistanceFilteredList  = [contour.tolist() for contour in centroidDistanceFiltered ]
        
        # Assert
        self.assertEqual(centroidDistanceFilteredList, [contourCenter5050.tolist()])

    def testTouchEdgeFilter(self):
        #Arrange
        contourEdge = np.array([[[0,50]],[[50,100]],[[100,100]],[[100,50]]])
        contourMiddle = np.array([[[10,20]],[[20,10]],[[10,10]],[[20,20]]])
        contours = [contourEdge, contourMiddle]

        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)

        #Act
        touchEdgeFiltered = filtrator.touchEdgeFilter(contours)
        touchEdgeFilteredList = [contour.tolist() for contour in touchEdgeFiltered]

        #Assert
        self.assertEqual(touchEdgeFilteredList, [contourMiddle.tolist()])

if __name__ == '__main__':
    unittest.main()
