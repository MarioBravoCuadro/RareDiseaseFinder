from abc import ABCMeta
from abc import abstractmethod
class IWorkflow(metaclass=ABCMeta):
    @abstractmethod
    def getSteps(self):
        pass
    @abstractmethod
    def getAvaliableSteps(self):
        pass
