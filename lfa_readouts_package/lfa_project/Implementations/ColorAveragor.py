import cv2 as cv
import numpy as np

class ColorAveragor():

    def __init__(self, printer, image, contour):
        self.printer = printer
        self.image = image
        self.contour = contour

    def average_color(self):
        mask = np.zeros(self.image.shape[:2], np.uint8)

        cv.drawContours(mask, [self.contour], 0, 255, -1)

        masked_image = cv.bitwise_and(self.image, self.image, mask=mask)

        avg_color = cv.mean(masked_image, mask=mask)

        self.printer.write_file("RGB:" + str(avg_color))

        return avg_color
