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

    def test_select_contour_no_contours(self):
        #Arrange
        selector = HierarchicalSelector(self.printer, self.image, self.contours)

        #Act and Assert
        with self.assertRaises(Exception) as e:
            selector.select_contour()
        self.assertEqual(str(e.exception), "No contours to select from after deepsearch. Terminating program.")

    def test_select_contour_one_contour(self):
        #Arrange
        contour_1 = np.array([[10,10],[50,10],[50,50],[10,50]])
        self.contours.append(contour_1)
        selector = HierarchicalSelector(self.printer, self.image, self.contours)

        #Act
        selected_contour = selector.select_contour()

        #Assert
        self.assertEqual(selected_contour.tolist(), self.contours[0].tolist())

    #selectOuterMost() is implicitly tested here as well
    def test_select_contour_many_contours(self):
        #Arrange
        contour_larger = np.array([[10,10],[50,10],[50,50],[10,50]])
        contour_smaller = np.array([[20,20],[30,20],[30,30],[20,30]])
        self.contours.append(contour_larger)
        self.contours.append(contour_smaller)
        selector = HierarchicalSelector(self.printer, self.image, self.contours)

        #Act
        outermost_contour = selector.select_outermost(self.contours)

        #Assert
        self.assertIsNotNone(outermost_contour)
        self.assertEqual(outermost_contour.tolist(), self.contours[0].tolist())

if __name__ == '__main__':
    unittest.main()
