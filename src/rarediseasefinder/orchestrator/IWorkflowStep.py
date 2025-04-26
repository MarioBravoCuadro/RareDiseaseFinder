
from abc import ABCMeta
from abc import abstractmethod
class IWorkflowStep(metaclass=ABCMeta):

    @abstractmethod
    def getStatus(self):
        pass
    @abstractmethod
    def process(self):
        pass
    @abstractmethod
    def revert(self):
        pass