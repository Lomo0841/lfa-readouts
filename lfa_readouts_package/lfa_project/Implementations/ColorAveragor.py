import cv2 as cv
import numpy as np

class ColorAveragor():

    def binaryMask(self, image, contour):
        mask = np.zeros(image.shape[:2], np.uint8)

        cv.drawContours(mask, [contour], 0, 255, -1)

        masked_img = cv.bitwise_and(image, image, mask=mask)

        avg_color = cv.mean(masked_img, mask=mask)

        #SHOULD BE MOVED TO A PRINTER CLASS
        print(avg_color)

    def averageColor(self, image, contour):
        self.binaryMask(image, contour)

