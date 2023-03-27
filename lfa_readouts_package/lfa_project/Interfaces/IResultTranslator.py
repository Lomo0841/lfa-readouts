from abc import ABC, abstractmethod

class IResultTranslator(ABC):

    @abstractmethod
    def translate_result(self):
        pass
    