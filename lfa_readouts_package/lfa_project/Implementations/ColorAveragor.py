import cv2 as cv
import numpy as np

class ColorAveragor():

    def __init__(self, printer, image, contour):
        self._printer = printer
        self._image = image
        self._contour = contour

    def average_color(self):
        mask = np.zeros(self._image.shape[:2], np.uint8)

        cv.drawContours(mask, [self._contour], 0, 255, -1)

        masked_image = cv.bitwise_and(self._image, self._image, mask=mask)

        avg_color = cv.mean(masked_image, mask=mask)

        self._printer.write_file("RGB: (" + str(avg_color[2]) + ", " + str(avg_color[1]) + ", " + str(avg_color[0]) + ")")

        return avg_color
