import unittest
from unittest.mock import MagicMock
import numpy as np
from lfa_project.Implementations.FilterOnConditions import FilterOnConditions

class FilterOnConditionsTest(unittest.TestCase):

    def setUp(self):
        #Arrange
        self.printer = MagicMock()
        self.config = MagicMock()
        self.image = np.zeros((100,100), np.uint8)

    def test_area_filter(self):
        #Arrange
        contour_over_50 = np.array([[50,50], [100,50], [100,100], [50,100]])
        contour_under_50 = np.array([[1,1], [1,2], [2,1], [2,2]])

        contours = [contour_over_50, contour_under_50]

        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)

        #Act
        area_filtered = filtrator.area_filter(contours, 50)
        area_filtered_list = [contour.tolist() for contour in area_filtered]

        #Assert
        self.assertEqual(area_filtered_list, [contour_over_50.tolist()])

    def test_convexity_defect_filter(self):
        #Arrange
        contour_with_convexity_defect = np.array([[0,0], [100,0], [50,50], [100,100], [0,100]])
        contour_without_convexity_defect = np.array([[200,200], [250,200], [250,250], [200,250]])
        contours = [contour_with_convexity_defect, contour_without_convexity_defect]
        max_depth = 50
        
        #Act
        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)
        convexity_defect_filtered = filtrator.convexity_defect_filter(contours, max_depth)
        convexity_defect_filtered_list = [contour.tolist() for contour in convexity_defect_filtered]

        #Assert
        self.assertEqual(convexity_defect_filtered_list, [contour_without_convexity_defect.tolist()])


    def test_centroid_distance_filter(self):
        # Arrange
        expected_centrum_x = 50
        expected_centrum_y = 50
        max_distance_from_centrum = 10
        
        contour_center_5050 = np.array([[40, 40], [60, 40], [60, 60], [40, 60]])
        contour_center_2525 = np.array([[20, 20], [30, 20], [30, 30], [20, 30]])
        contours = [contour_center_5050, contour_center_2525]
        
        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)
        
        # Act
        centroid_distance_filtered = filtrator.centroid_distance_filter(contours, expected_centrum_x, expected_centrum_y, max_distance_from_centrum)
        centroid_distance_filtered_list  = [contour.tolist() for contour in centroid_distance_filtered ]
        
        # Assert
        self.assertEqual(centroid_distance_filtered_list, [contour_center_5050.tolist()])

    def test_touch_edge_filter(self):
        #Arrange
        contour_edge = np.array([[[0,50]],[[50,100]],[[100,100]],[[100,50]]])
        contour_middle = np.array([[[10,20]],[[20,10]],[[10,10]],[[20,20]]])
        contours = [contour_edge, contour_middle]

        filtrator = FilterOnConditions(self.printer, self.config, self.image, contours)

        #Act
        touch_edge_filtered = filtrator.touch_edge_filter(contours)
        touch_edge_filtered_list = [contour.tolist() for contour in touch_edge_filtered]

        #Assert
        self.assertEqual(touch_edge_filtered_list, [contour_middle.tolist()])

if __name__ == '__main__':
    unittest.main()
