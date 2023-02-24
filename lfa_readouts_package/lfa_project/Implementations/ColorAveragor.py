import cv2 as cv
import numpy as np

class ColorAveragor():

    def binaryMask(self, image, contour):
        mask = np.zeros(image.shape[:2], np.uint8)

        cv.drawContours(mask, [contour], 0, 255, -1)

        cv.imshow("hej2", mask)

        masked_img = cv.bitwise_and(image, image, mask=mask)

        avg_color = cv.mean(masked_img, mask=mask)

        cv.imshow("hej", masked_img)
        print(avg_color)

    def averageColor():
        pass

