import unittest
from unittest.mock import MagicMock
import numpy as np
from lfa_project.Implementations.MaxRGB import MaxRGB

class MaxRGBTest(unittest.TestCase):
        
    def setUp(self):
        #Arrange
        self.printer = MagicMock()

    def test_normalize(self):
        #Arrange
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :, 0] = 200

        white_balancer = MaxRGB(self.printer, img)

        #Act
        result = white_balancer.normalize(img)

        #Assert
        self.assertTrue((result[:, :, 0] > result[:, :, 1]).all())
        self.assertTrue((result[:, :, 0] > result[:, :, 2]).all())

if __name__ == '__main__':
    unittest.main()