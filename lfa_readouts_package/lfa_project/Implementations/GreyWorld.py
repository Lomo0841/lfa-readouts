from lfa_project.Interfaces.IWhiteBalancing import IWhiteBalancing
import cv2 as cv
import numpy as np

class GreyWorld(IWhiteBalancing):

    def __init__(self, printer, image):
        self.printer = printer
        self.image = image

    def whiteBalance(self):
        balanced = self.normalize(self.image)

        self.printer.write_image(balanced, "White balanced")

        return balanced

    def normalize(self, img):
        labImg = cv.cvtColor(img, cv.COLOR_BGR2LAB)

        lMean, aMean, bMean, _ = cv.mean(labImg)

        lScale = 128 / lMean
        aScale = 128 / aMean
        bScale = 128 / bMean

        labImg[:, :, 0] = cv.multiply(labImg[:, :, 0], lScale)
        labImg[:, :, 1] = cv.multiply(labImg[:, :, 1], aScale)
        labImg[:, :, 2] = cv.multiply(labImg[:, :, 2], bScale)

        balancedImg = cv.cvtColor(labImg, cv.COLOR_LAB2BGR)

        return balancedImg


