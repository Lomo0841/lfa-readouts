import cv2 as cv
from lfa_project.Interfaces.IContourDetector import IContourDetector

class BlurThresholdContourDetector(IContourDetector):

    def __init__(self, printer, config, image):
        self.printer = printer
        self.image = image
        self.config = config

    def detect_contours(self):
        section = "ContourDetection"
        kernel_size = self.config.get_config_int(section, "kernelSize")

        blurred_image = self.blur(self.image, kernel_size)

        thresholded_image = self.threshold(blurred_image)

        self.printer.write_image(thresholded_image, "ThresholdedImage")

        contours = self.find_contours(thresholded_image)

        self.printer.write_image(self.image, "AllContours", contours)

        return contours

    def blur(self, image, size):
        blur = cv.GaussianBlur(image, (size, size), 0)

        return blur

    def threshold(self, blur):
        grey_scale = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

        ret, thresholded_image = cv.threshold(grey_scale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        return thresholded_image
    
    def find_contours(self, thresholded_image):
        contours, _ = cv.findContours(thresholded_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours


