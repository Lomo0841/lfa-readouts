import cv2 as cv
import numpy as np
import pupil_apriltags as apriltag
from lfa_project.Interfaces.IRoiExtractor import IRoiExtractor

class AprilTagsExtractor(IRoiExtractor):

    #maybe config
    def __init__(self, printer, image):
        self._printer = printer
        self._image = image
        #self.config = config


    def extract_rois(self):
        #section = "CropRoi"
        #x = self.config.get_config_int(section, "x")
        #y = self.config.get_config_int(section, "y")
        #h = self.config.get_config_int(section, "h")
        #w = self.config.get_config_int(section, "w")

        image_grey_scale = self._grey_scale(self._image) 
        
        de_warped = self._de_warp(self._image, image_grey_scale)
        
        #cropped = self.crop_roi(de_warped, x, y, h, w)

        self._printer.write_image(de_warped, "Roi")

        return de_warped
    
    def _grey_scale(self, image):
        
        grey_scale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        return grey_scale
    
    def _de_warp(self, original_image, grey_scale):

        detections = self._detect_april_tags(grey_scale)
        
        if len(detections) < 4:
            raise Exception("Could not find all 4 AprilTags")

        for det in detections:
            if det.tag_id == 0:
                upper_left = det.corners[2].astype(int)
            if det.tag_id == 1:
                upper_right = det.corners[3].astype(int)
            if det.tag_id == 2:
                lower_left = det.corners[1].astype(int)
            if det.tag_id == 4: 
                lower_right = det.corners[0].astype(int)

        #https://theailearner.com/tag/cv2-warpperspective/
        width_upper = np.sqrt(((upper_left[0] - upper_right[0]) ** 2) + ((upper_left[1] - upper_right[1]) ** 2))
        width_lower = np.sqrt(((lower_left[0] - lower_right[0]) ** 2) + ((lower_left[1] - lower_right[1]) ** 2))
        max_width = max(int(width_upper), int(width_lower))
 
 
        height_left = np.sqrt(((upper_left[0] - lower_left[0]) ** 2) + ((upper_left[1] - lower_left[1]) ** 2))
        height_right = np.sqrt(((lower_right[0] - upper_right[0]) ** 2) + ((lower_right[1] - upper_right[1]) ** 2))
        max_height = max(int(height_left), int(height_right))

        original_points = np.float32([upper_left, lower_left, lower_right, upper_right])
        transformed_points = np.float32([[0, 0], [0, max_height - 1], [max_width - 1, max_height - 1],[max_width - 1, 0]]) 

        transform = cv.getPerspectiveTransform(original_points, transformed_points)

        de_warped_image = cv.warpPerspective(original_image, transform,(max_width, max_height),flags=cv.INTER_LINEAR)

        return de_warped_image


    def _crop_roi(image, x, y, h, w):

        return image[y:y+h, x:x+w]

    
    def _detect_april_tags(self, grey_scale):

        detector = apriltag.Detector("tag36h11")

        detections = detector.detect(grey_scale)

        return detections