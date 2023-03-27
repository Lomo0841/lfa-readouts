from lfa_project.Interfaces.IWhiteBalancing import IWhiteBalancing
import cv2 as cv
import numpy as np

class MaxRGB(IWhiteBalancing):

    def __init__(self, printer, image):
        self.printer = printer
        self.image = image

    def whiteBalance(self):
        normalizedImg = self.normalize(self.image)

        convertedImg = self.convert(normalizedImg)

        self.printer.write_image(convertedImg, "White balanced")

        return convertedImg

    def normalize(self, img):
        b, g, r = cv.split(img)
        maxVals = np.maximum(np.maximum(r, g), b)

        rNorm = r / maxVals
        gNorm = g / maxVals
        bNorm = b / maxVals

        balancedImg = cv.merge((bNorm, gNorm, rNorm))

        return balancedImg

    def convert(self, img):
        converted = cv.convertScaleAbs(img * 255)

        return converted
