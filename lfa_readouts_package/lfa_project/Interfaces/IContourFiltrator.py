from abc import ABC, abstractmethod

class IContourFiltrator(ABC):

    @abstractmethod
    def filterContours(self):
        pass
