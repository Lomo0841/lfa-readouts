import cv2 as cv
from lfa_project.Interfaces.IContourDetector import IContourDetector

class BlurThresholdContourDetector(IContourDetector):

    def __init__(self, printer, config, image):
        self._printer = printer
        self._image = image
        self._config = config

    def detect_contours(self):
        section = "ContourDetection"
        kernel_size = self._config.get_config_int(section, "kernelSize")

        blurred_image = self._blur(self._image, kernel_size)

        thresholded_image = self._threshold(blurred_image)

        self._printer.write_image(thresholded_image, "ThresholdedImage")

        contours = self._find_contours(thresholded_image)

        self._printer.write_image(self._image, "AllContours", contours)

        return contours

    def _blur(self, image, size):
        blur = cv.GaussianBlur(image, (size, size), 0)

        return blur

    def _threshold(self, blur):
        grey_scale = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

        ret, thresholded_image = cv.threshold(grey_scale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        return thresholded_image
    
    def _find_contours(self, thresholded_image):
        contours, _ = cv.findContours(thresholded_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours


