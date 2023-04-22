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

    def test_color_averagor_green(self):
        #Arrange
        color_averagor = ColorAveragor(self.printer, self.image, self.contour)
        
        #Act
        average = color_averagor.average_color()
        
        #Assert
        self.assertAlmostEqual(average, (0.0, 255.0 ,0.0 ,0.0))

if __name__ == '__main__':
    unittest.main()