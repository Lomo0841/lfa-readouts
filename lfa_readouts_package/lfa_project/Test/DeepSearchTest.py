import cv2 as cv
import numpy as np
import unittest
from unittest.mock import MagicMock
from lfa_project.Implementations.DeepSearch import DeepSearch

class DeepSearchTest(unittest.TestCase):

    def setUp(self):
        #Arrange
        self.printer = MagicMock()
        self.image = np.zeros((1000, 1000, 3), dtype=np.uint8)
        cv.circle(self.image, (100, 100), 50, (255, 255, 255), -1)

    def test_run_all_contours(self):
        #Arrange
        deep_search = DeepSearch(self.printer, self.image)

        #Act
        all_contours = deep_search.run_all_contours(0, 255, self.image)

        #Assert
        self.assertEqual(len(all_contours), 255)

    def test_analyse_histogram(self):
        #Arrange
        deep_search = DeepSearch(self.printer, self.image)

        #Act
        min, max = deep_search.analyse_histogram(self.image)

        #Assert
        self.assertEqual(min, 0)
        self.assertEqual(max, 255)


if __name__ == '__main__':
    unittest.main()

