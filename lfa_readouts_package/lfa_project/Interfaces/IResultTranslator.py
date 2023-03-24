from abc import ABC, abstractmethod

class IResultTranslator(ABC):

    @abstractmethod
    def translateResult(self):
        pass
    