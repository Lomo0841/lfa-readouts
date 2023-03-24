from abc import ABC, abstractmethod

class IContourFiltrator(ABC):

    @abstractmethod
    def filter_contours(self):
        pass
