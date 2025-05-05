from abc import ABCMeta
from abc import abstractmethod
class IWorkflow(metaclass=ABCMeta):
    @abstractmethod
    def get_steps(self):
        pass
    @abstractmethod
    def get_available_steps(self):
        pass
