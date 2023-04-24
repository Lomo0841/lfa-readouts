from lfa_project.Interfaces.IWhiteBalancing import IWhiteBalancing
import cv2 as cv
import numpy as np

class GreyWorld(IWhiteBalancing):

    def __init__(self, printer, image):
        self._printer = printer
        self._image = image

    def white_balance(self):
        balanced = self._normalize(self._image)

        self._printer.write_image(balanced, "White balanced")

        return balanced

    def _normalize(self, img):
        avg_b = np.mean(img[:, :, 0])
        avg_g = np.mean(img[:, :, 1])
        avg_r = np.mean(img[:, :, 2])
    
        grey_value = np.mean([avg_b, avg_g, avg_r])
        scale_b = grey_value / avg_b
        scale_g = grey_value / avg_g
        scale_r = grey_value / avg_r
        
        #Applying the scales to all pixels
        img[:, :, 0] = np.clip(img[:, :, 0] * scale_b, 0, 255).astype(np.uint8)
        img[:, :, 1] = np.clip(img[:, :, 1] * scale_g, 0, 255).astype(np.uint8)
        img[:, :, 2] = np.clip(img[:, :, 2] * scale_r, 0, 255).astype(np.uint8)

        return img
