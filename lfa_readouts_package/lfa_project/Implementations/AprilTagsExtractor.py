import cv2 as cv
import numpy as np
import pupil_apriltags as apriltag
from lfa_project.Interfaces.IRoiExtractor import IRoiExtractor
import time as t

class AprilTagsExtractor(IRoiExtractor):

    def __init__(self, printer, image):
        self.printer = printer
        self.image = image

    #Remember to dewarp in 3d space
    #Can we use only one detection?
    def extractRois(self) -> cv.Mat:

        imageGreyScale = self.greyScale(self.image) 
        
        deWarped = self.deWarp(self.image, imageGreyScale)

        #greyScaleDewarped = self.greyScale(deWarped)
        
        #cropped = self.cropRoi(deWarped, greyScaleDewarped)

        self.printer.write_image(deWarped, "Roi")

        return deWarped
    
    def greyScale(self, image) -> cv.Mat:
        
        greyScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        return greyScale
    
    #Extracted to more methods? 
    def deWarp(self, originalImage, greyscale) -> cv.Mat:

        detections = self.detectAprilTags(greyscale)

        for det in detections:
            if det.tag_id == 0:
                upperLeft = det.corners[2].astype(int)
            if det.tag_id == 1:
                upperRight = det.corners[3].astype(int)
            if det.tag_id == 2:
                lowerLeft = det.corners[1].astype(int)
            if det.tag_id == 4: 
                lowerRight = det.corners[0].astype(int)

        cv.imshow("corners???", originalImage)

        #https://theailearner.com/tag/cv2-warpperspective/
        widthUpper = np.sqrt(((upperLeft[0] - upperRight[0]) ** 2) + ((upperLeft[1] - upperRight[1]) ** 2))
        widthLower = np.sqrt(((lowerLeft[0] - lowerRight[0]) ** 2) + ((lowerLeft[1] - lowerRight[1]) ** 2))
        maxWidth = max(int(widthUpper), int(widthLower))
 
 
        heightLeft = np.sqrt(((upperLeft[0] - lowerLeft[0]) ** 2) + ((upperLeft[1] - lowerLeft[1]) ** 2))
        heightRight = np.sqrt(((lowerRight[0] - upperRight[0]) ** 2) + ((lowerRight[1] - upperRight[1]) ** 2))
        maxHeight = max(int(heightLeft), int(heightRight))

        originalPoints = np.float32([upperLeft, lowerLeft, lowerRight, upperRight])
        transformedPoints = np.float32([[0, 0], [0, maxHeight - 1], [maxWidth - 1, maxHeight - 1],[maxWidth - 1, 0]]) 

        transform = cv.getPerspectiveTransform(originalPoints, transformedPoints)

        deWarpedImage = cv.warpPerspective(originalImage, transform,(maxWidth, maxHeight),flags=cv.INTER_LINEAR)
        cv.imshow("Dewarped?", deWarpedImage)

        return deWarpedImage


        
        """ #Converting the corners to a matrix where each row corresponds to a corner
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

            return rotatedImage """

    """   def cropRoi(self, image, greyscale) -> cv.Mat: 
        
        detections = self.detectAprilTags(greyscale)

        for det in detections:
            if det.tag_id == 0:
                upperleft = det.corners[2].astype(int)
                #cv.circle(image, det.corners[0].astype(int), radius=10, color=(255,0,0), thickness=2)
                #cv.circle(image, det.corners[1].astype(int), radius=10, color=(0,255,0), thickness=2)
                #cv.circle(image, det.corners[2].astype(int), radius=10, color=(0,0,255), thickness=2)
            if det.tag_id == 1:
                pass
            if det.tag_id == 2:
                pass
            if det.tag_id == 4: 
                lowerright = det.corners[0].astype(int)

        #cv.imshow("corners", image)
        croppedImage = image[upperleft[1]:lowerright[1], upperleft[0]:lowerright[0]]

        return croppedImage """
    
    def detectAprilTags(self, greyscale):

        detector = apriltag.Detector("tag36h11")

        detections = detector.detect(greyscale)

        return detections