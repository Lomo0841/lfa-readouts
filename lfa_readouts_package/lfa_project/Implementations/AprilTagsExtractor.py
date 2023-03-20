import cv2 as cv
import numpy as np
import pupil_apriltags as apriltag
from lfa_project.Interfaces.IRoiExtractor import IRoiExtractor
import time as t

class AprilTagsExtractor(IRoiExtractor):

    #maybe config
    def __init__(self, printer, image):
        self.printer = printer
        self.image = image
        #self.config = config


    def extractRois(self):
        #section = "CropRoi"
        #x = self.config.getConfigInt(section, "x")
        #y = self.config.getConfigInt(section, "y")
        #h = self.config.getConfigInt(section, "h")
        #w = self.config.getConfigInt(section, "w")

        imageGreyScale = self.greyScale(self.image) 
        
        deWarped = self.deWarp(self.image, imageGreyScale)
        
        #cropped = self.cropRoi(deWarped, x, y, h, w)

        self.printer.write_image(deWarped, "Roi")

        return deWarped
    
    def greyScale(self, image):
        
        greyScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        return greyScale
    
    def deWarp(self, originalImage, greyscale):

        detections = self.detectAprilTags(greyscale)
        
        if len(detections) < 4:
            raise Exception("Could not find all 4 AprilTags")

        for det in detections:
            if det.tag_id == 0:
                upperLeft = det.corners[2].astype(int)
            if det.tag_id == 1:
                upperRight = det.corners[3].astype(int)
            if det.tag_id == 2:
                lowerLeft = det.corners[1].astype(int)
            if det.tag_id == 4: 
                lowerRight = det.corners[0].astype(int)

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

        return deWarpedImage


    def cropRoi(image, x, y, h, w):

        return image[y:y+h, x:x+w]

    
    def detectAprilTags(self, greyscale):

        detector = apriltag.Detector("tag36h11")

        detections = detector.detect(greyscale)

        return detections