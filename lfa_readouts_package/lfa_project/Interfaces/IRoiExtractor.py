from abc import ABC, abstractmethod
import cv2 as cv

class IRoiExtractor(ABC):

    @abstractmethod
    def extractRois(self, image) -> cv.Mat:
        pass
