import pandas as pd

from ...biodata_providers.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from ...orchestrator.IWorkflowStep import IWorkflowStep


class SelleckchemWorkflowStep(IWorkflowStep):
    name = None
    description = None
    processor = None
    params = None

    def __init__(self,params):
        self.name = "Selleckchem step"
        self.description = "Gets links from selleckchem for x term"
        self.processor = SelleckchemProcessor()
        self.params = params

    def get_status_code(self)->int:
        return self.processor.get_status_code()

    def process(self)->dict:
        return self.processor.fetch(self.params)

    def revert(self):
        pass