from abc import ABC, abstractmethod

class IRoiExtractor(ABC):

    @abstractmethod
    def extract_rois(self):
        pass
