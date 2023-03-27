from lfa_project.Interfaces.IWhiteBalancing import IWhiteBalancing
import cv2 as cv

class GreyWorld(IWhiteBalancing):

    def __init__(self, printer, image):
        self.printer = printer
        self.image = image

    def white_balance(self):
        balanced = self.normalize(self.image)

        self.printer.write_image(balanced, "White balanced")

        return balanced

    def normalize(self, img):
        lab_img = cv.cvtColor(img, cv.COLOR_BGR2LAB)

        l_mean, a_mean, b_mean, _ = cv.mean(lab_img)

        l_scale = 128 / l_mean
        a_scale = 128 / a_mean
        b_scale = 128 / b_mean

        lab_img[:, :, 0] = cv.multiply(lab_img[:, :, 0], l_scale)
        lab_img[:, :, 1] = cv.multiply(lab_img[:, :, 1], a_scale)
        lab_img[:, :, 2] = cv.multiply(lab_img[:, :, 2], b_scale)

        balanced_img = cv.cvtColor(lab_img, cv.COLOR_LAB2BGR)

        return balanced_img


