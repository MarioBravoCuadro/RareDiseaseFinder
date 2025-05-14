from ...biodata_providers.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from ...orchestrator.IWorkflowStep import IWorkflowStep


class SelleckchemWorkflowStep(IWorkflowStep):
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        self.name = "Selleckchem step"
        self.description = "Gets links from selleckchem for x term"
        self.processor = SelleckchemProcessor()

    def set_filters(self, filters):
        self.filters = filters

    def get_status_code(self)->int:
        return self.processor.get_status_code()

    def process(self)->dict:
        return self.processor.fetch(self.filters)

    def revert(self):
        pass