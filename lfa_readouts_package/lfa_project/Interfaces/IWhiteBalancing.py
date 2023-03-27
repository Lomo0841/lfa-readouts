from abc import ABC, abstractmethod

class IWhiteBalancing(ABC):

    @abstractmethod
    def white_balance(self):
        pass