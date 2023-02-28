import cv2 as cv
import numpy as np
import pupil_apriltags as apriltag
from lfa_project.Interfaces.IContourDetector import IContourDetector

class BlurThresholdContourDetector(IContourDetector):

    def __init__(self, printer, image):
        self.printer = printer
        self.image = image

    
    #Should return a list of pictures
    def detectContours(self) -> cv.Mat:
        blurredImage = self.blur(self.image)

        thresholdedImage = self.threshold(blurredImage)

        self.printer.write_image(thresholdedImage, "ThresholdedImage")

        contours = self.findContours(thresholdedImage)

        self.printer.write_image(self.image, "AllContours", contours)

        return contours


    def blur(self, image) -> cv.Mat:
        blur = cv.GaussianBlur(image, (5, 5), 0)

        return blur

    def threshold(self, image) -> cv.Mat:
        greyScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        ret, thresholdedImage = cv.threshold(greyScale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        return thresholdedImage
    
    def findContours(self, thresholdedImage) -> cv.Mat:
        contours, hierarchy = cv.findContours(thresholdedImage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours


