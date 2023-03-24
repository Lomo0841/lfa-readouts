import unittest
from unittest.mock import MagicMock
import cv2 as cv
import numpy as np
from lfa_project.Implementations.ColorAveragor import ColorAveragor

class ColorAveragorTest(unittest.TestCase):

    def setUp(self):
        #Arrange
        self.printer = MagicMock()
        self.image = np.zeros((100, 100, 3), np.uint8)
        self.image[:, :, 1] = 255
        self.contour = np.array([[10, 10], [90, 10], [90, 90], [10, 90]], dtype=np.int32)

    def testColorAveragorGreen(self):
        #Arrange
        mask = np.zeros(self.image.shape[:2], np.uint8)
        cv.drawContours(mask, [self.contour], 0, 255, -1)
        self.image[mask == 255] = (0, 255, 0)
        colorAveragor = ColorAveragor(self.printer, self.image, self.contour)
        
        #Act
        average = colorAveragor.averageColor()
        
        #Assert
        self.assertAlmostEqual(average, (0.0, 255.0 ,0.0 ,0.0))

if __name__ == '__main__':
    unittest.main()