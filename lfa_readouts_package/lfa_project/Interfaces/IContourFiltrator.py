from abc import ABC, abstractmethod
import cv2 as cv

class IContourFiltrator(ABC):

    @abstractmethod
    def filterContours(self, image) -> cv.Mat:
        pass
