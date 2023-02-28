from abc import ABC, abstractmethod
import cv2 as cv

class IResultTranslator(ABC):

    @abstractmethod
    def translateResult(self):
        pass
    