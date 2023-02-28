from abc import ABC, abstractmethod
import cv2 as cv

class IContourDetector(ABC):

    @abstractmethod
    def detectContours(self):
        pass

