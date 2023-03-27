from abc import ABC, abstractmethod

class IContourDetector(ABC):

    @abstractmethod
    def detectContours(self):
        pass
