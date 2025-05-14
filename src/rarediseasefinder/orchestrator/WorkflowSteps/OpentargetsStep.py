from src.rarediseasefinder.biodata_providers.opentargets.OpenTargetsProcessor import OpenTargetsProcessor
from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep


class OpentargetsStep(IWorkflowStep):
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        self.name = "OpenTargets step"
        self.description = "Fetches x data from OpenTargets API"
        self.processor = OpenTargetsProcessor()

    def set_filters(self, filters):
        self.filters = filters

    def get_status_code(self)->int:
        return self.processor.get_status_code()

    def process(self)-> dict:
        return self.processor.fetch(self.filters)

    def revert(self):
        pass