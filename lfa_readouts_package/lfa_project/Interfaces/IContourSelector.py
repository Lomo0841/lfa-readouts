from abc import ABC, abstractmethod

class IContourSelector(ABC):

    @abstractmethod
    def select_contour(self):
        pass
    