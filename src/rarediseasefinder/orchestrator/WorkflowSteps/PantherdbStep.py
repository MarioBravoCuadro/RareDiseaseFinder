from src.rarediseasefinder.biodata_providers.phanterdb.PhanterProcessor import PhanterProcessor
from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep


class PantherdbStep(IWorkflowStep):
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        self.name = "Panther step"
        self.description = "Fetches x data from Panther API"
        self.processor = PhanterProcessor()

    def set_filters(self, filters):
        self.filters = filters

    def get_status_code(self)->int:
        return self.processor.get_status_code()

    def process(self)-> dict:
        return self.processor.fetch(self.filters)

    def revert(self):
        pass