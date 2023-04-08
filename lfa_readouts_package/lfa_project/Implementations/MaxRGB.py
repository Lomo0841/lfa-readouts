from lfa_project.Interfaces.IWhiteBalancing import IWhiteBalancing
import cv2 as cv
import numpy as np

class MaxRGB(IWhiteBalancing):

    def __init__(self, printer, image):
        self._printer = printer
        self._image = image

    def white_balance(self):
        normalized_img = self._normalize(self._image)

        converted_img = self._convert_to_8_bit(normalized_img)

        self._printer.write_image(converted_img, "White balanced")

        return converted_img

    def _normalize(self, img):
        b, g, r = cv.split(img)
        max_values = np.maximum(np.maximum(r, g), b)

        r_norm = r / max_values
        g_norm = g / max_values
        b_norm = b / max_values

        balanced_img = cv.merge((b_norm, g_norm, r_norm))

        return balanced_img

    def _convert_to_8_bit(self, img):
        converted = cv.convertScaleAbs(img * 255)

        return converted
