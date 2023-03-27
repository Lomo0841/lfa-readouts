from abc import ABC, abstractmethod

class IContourDetector(ABC):

    @abstractmethod
    def detect_contours(self):
        pass
