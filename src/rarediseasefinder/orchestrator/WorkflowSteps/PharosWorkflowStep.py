import pandas as pd

from ...biodata_providers.pharos.PharosProcessor import PharosProcessor
from ...orchestrator.IWorkflowStep import IWorkflowStep


class PharosWorkflowStep(IWorkflowStep):
    name = None
    description = None
    processor = None
    params = None

    def __init__(self,params):
        self.name = "Pharos step"
        self.description = "Fetches x data from Pharos API"
        self.processor = PharosProcessor()
        self.params = params

    def get_status_code(self)->int:
        return self.processor.get_status_code()

    def process(self)-> dict:
        return self.processor.fetch(self.params)

    def revert(self):
        pass