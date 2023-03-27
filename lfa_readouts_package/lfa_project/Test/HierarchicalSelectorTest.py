import unittest
import cv2 as cv
import numpy as np
from unittest.mock import MagicMock
from lfa_project.Implementations.HierarchicalSelector import HierarchicalSelector

class HierarchicalSelectorTest(unittest.TestCase):
    
    def setUp(self):
        #Arrange
        self.image = np.zeros((100,100), np.uint8)
        self.contours = []
        self.printer = MagicMock()

    def testSelectContourNoContours(self):
        #Arrange
        selector = HierarchicalSelector(self.printer, self.image, self.contours)

        #Act and Assert
        with self.assertRaises(Exception) as e:
            selector.selectContour()
        self.assertEqual(str(e.exception), "No contours to select from after deepsearch. Terminating program.")

    def testSelectContourOneContour(self):
        #Arrange
        contour1 = np.array([[10,10],[50,10],[50,50],[10,50]])
        self.contours.append(contour1)
        selector = HierarchicalSelector(self.printer, self.image, self.contours)

        #Act
        selectedContour = selector.selectContour()

        #Assert
        self.assertEqual(selectedContour.tolist(), self.contours[0].tolist())

    #selectOuterMost() is implicitly tested here as well
    def testSelectContourManyContours(self):
        #Arrange
        contourLarger = np.array([[10,10],[50,10],[50,50],[10,50]])
        contourSmaller = np.array([[20,20],[30,20],[30,30],[20,30]])
        self.contours.append(contourLarger)
        self.contours.append(contourSmaller)
        selector = HierarchicalSelector(self.printer, self.image, self.contours)

        #Act
        outermostContour = selector.selectOutermost(self.contours)

        #Assert
        self.assertIsNotNone(outermostContour)
        self.assertEqual(outermostContour.tolist(), self.contours[0].tolist())




if __name__ == '__main__':
    unittest.main()
