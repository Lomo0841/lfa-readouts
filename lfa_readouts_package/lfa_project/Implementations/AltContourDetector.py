import cv2 as cv
from lfa_project.Interfaces.IContourDetector import IContourDetector

class AltContourDetector(IContourDetector):

    def __init__(self, printer, config, image):
        self.printer = printer
        self.image = image
        self.config = config
        

    def detectContours(self):
        section = "ContourDetection"
        kernelSize = self.config.getConfigInt(section, "kernelSize")

        blurredImage = self.blur(self.image, kernelSize)

        thresholdedImage = self.threshold(blurredImage)

        self.printer.write_image(thresholdedImage, "ThresholdedImage")

        contours = self.findContours(thresholdedImage)

        self.printer.write_image(self.image, "AllContours", contours)

        return contours

    def blur(self, image, size):
        blur = cv.medianBlur(image, size)

        return blur

    def threshold(self, blur):
        greyScale = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

        ret, thresholdedImage = cv.threshold(greyScale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        return thresholdedImage

    def findContours(self, thresholdedImage):
        contours, _ = cv.findContours(thresholdedImage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours