from abc import ABC, abstractmethod

class IWhiteBalancing(ABC):

    @abstractmethod
    def whiteBalance(self):
        pass