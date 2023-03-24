from abc import ABC, abstractmethod

class IRoiExtractor(ABC):

    @abstractmethod
    def extractRois(self):
        pass
