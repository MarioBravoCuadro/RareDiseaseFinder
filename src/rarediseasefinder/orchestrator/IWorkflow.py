from abc import ABCMeta
from abc import abstractmethod
class IWorkflow(metaclass=ABCMeta):
    @abstractmethod
    def get_steps(self):
        pass
    @abstractmethod
    def check_if_all_steps_available(self):
        pass
