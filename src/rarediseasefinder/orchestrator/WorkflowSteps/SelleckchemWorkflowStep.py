import pandas as pd

from ...orchestrator.IWorkflowStep import IWorkflowStep
from ...selleckchem.SelleckchemProcessor import SelleckchemProcessor

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

    def getStatus(self)->str:
        return self.processor.getStatus()

    def process(self)->pd.DataFrame:
        return self.processor.obtener_links_selleckchem(self.params)

    def revert(self):
        pass