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

    def testRunAllContours(self):
        #Arrange
        deepSearch = DeepSearch(self.printer, self.image)

        #Act
        allContours = deepSearch.runAllContours(0, 255, self.image)

        #Assert
        self.assertEqual(len(allContours), 255)

    def testAnalyseHistogram(self):
        #Arrange
        deepSearch = DeepSearch(self.printer, self.image)

        #Act
        min, max = deepSearch.analyseHistogram(self.image)

        #Assert
        self.assertEqual(min, 0)
        self.assertEqual(max, 255)


if __name__ == '__main__':
    unittest.main()

