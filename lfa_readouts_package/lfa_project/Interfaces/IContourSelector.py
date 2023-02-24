from abc import ABC, abstractmethod
import cv2 as cv

class IContourSelector(ABC):

    @abstractmethod
    def selectContour(self, image) -> cv.Mat:
        pass
    