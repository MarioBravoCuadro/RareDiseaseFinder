import pandas as pd

from ...orchestrator.IWorkflowStep import IWorkflowStep
from ...biodata_providers.pharos import PharosProcessor

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

    def getStatus(self)->str:
        return self.processor.getStatus()

    def process(self)->pd.DataFrame:
        return self.processor.fetch(self.params)

    def revert(self):
        pass