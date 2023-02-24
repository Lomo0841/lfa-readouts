import cv2 as cv
import numpy as np
import pupil_apriltags as apriltag
from lfa_project.Interfaces.IRoiExtractor import IRoiExtractor

class AprilTagsExtractor(IRoiExtractor):

    #Remember to dewarp in 3d space
    def extractRois(self, image) -> cv.Mat:
        greyScale = self.greyScale(image)

        deWarped = self.deWarp(greyScale, image)

        cropped = self.cropRoi(deWarped, 1, 1, 1, 1)

        return deWarped
    
    def greyScale(self, image) -> cv.Mat:
        greyScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        return greyScale
    
    #Extracted to more methods? 
    def deWarp(self, greyScale, originalImage) -> cv.Mat:
        detector = apriltag.Detector("tag36h11")

        detections = detector.detect(greyScale)

        #Converting the corners to a matrix where each row corresponds to a corner
        tag_corners = detections[0].corners.reshape((4, 2))

        tag_id = detections[0].tag_id

        if tag_id == 0:
            #Get the coordinates of the two top corners
            top_corners = tag_corners[:2]

            #Calculate the angle between the two top corners and the horizontal axis
            angle = np.arctan2(top_corners[1][1] - top_corners[0][1], top_corners[1][0] - top_corners[0][0]) * 180 / np.pi

            #Creating rotationmatrix based on the center of the image and the calculated angle
            height, width = originalImage.shape[:2]
            center = (width // 2, height // 2)
            M = cv.getRotationMatrix2D(center, angle, 1.0)

            #Applying the rotationmatrix
            rotatedImage = cv.warpAffine(originalImage, M, (width, height))

            return rotatedImage

    def cropRoi(self, image, x, y, h, w) -> cv.Mat: 
        croppedImage = image[y:h+y, x:w+x]

        return croppedImage