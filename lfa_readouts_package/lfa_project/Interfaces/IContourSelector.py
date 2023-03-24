from abc import ABC, abstractmethod

class IContourSelector(ABC):

    @abstractmethod
    def selectContour(self):
        pass
    