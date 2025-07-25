from abc import ABCMeta
from abc import abstractmethod
class IWorkflowStep(metaclass=ABCMeta):

    @abstractmethod
    def get_status_code(self):
        pass
    @abstractmethod
    def process(self):
        pass
    @abstractmethod
    def revert(self):
        pass