import pandas as pd

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.PharosWorkflowStep import PharosWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep


class Workflow(IWorkflow):
    name = None
    description = None
    listOfSteps=None

    def __init__(self,gen_param):
        self.name = "Workflow for TFG"
        self.description = "Fetches x data from Pharos API x data from selleckchem"
        self.listOfSteps = {
            "Pharos data": {
                "Description": "Fetches x data from Pharos",
                "Object": PharosWorkflowStep(gen_param)
            },
            "Selleckchem data": {
                "Description": "Gets links from selleckchem for x term",
                "Object": SelleckchemWorkflowStep(gen_param)
            }
        }
        pass

    def get_steps(self)->dict:
        return self.listOfSteps

    def get_available_steps(self):
        return self.check_available_steps()

    def check_available_steps(self)->bool:
        for step in self.listOfSteps.values():
            if step["Object"].get_status_code() != 200:
                return False
        return True

    def steps_execution(self)-> list[pd.DataFrame]:
        pharos_data = self.listOfSteps.get("Pharos data")["Object"].process()
        selleckchem_data = self.listOfSteps.get("Selleckchem data")["Object"].process()

        workflow_result = [pharos_data,selleckchem_data]

        return workflow_result