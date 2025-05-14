from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor
from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep


class UniprotStep(IWorkflowStep):
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        self.name = "Uniprot step"
        self.description = "Fetches x data from Uniprot API"
        self.processor = UniprotProcessor()

    def set_filters(self, filters):
        self.filters = filters

    def get_status_code(self)->int:
        return self.processor.get_status_code()

    def process(self)-> dict:
        return self.processor.fetch(self.filters)

    def revert(self):
        pass