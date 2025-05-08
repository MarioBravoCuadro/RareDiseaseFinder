import json

from src.rarediseasefinder.biodata_providers.pharos.PharosProcessor import PharosProcessor
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
        pass

    def read_steps_from_filters(self):
        return

    def get_steps(self)->dict:
        return self.listOfSteps

    def check_if_all_steps_available(self):
        return self._check_available_steps()

    def _check_available_steps(self)->bool:
        for step in self.listOfSteps.values():
            if step["Object"].get_status_code() != 200:
                return False
        return True

    def steps_execution(self)-> list[dict]:
        instrucciones_procesador_pharos_json = self.add_search_id_to_json(self.get_json_from_route('Processors_JSONs/pharos.json'),"FANCA")
        pharos_step = PharosWorkflowStep(instrucciones_procesador_pharos_json)
        pharos_step.get_status_code()
        pharos_step.process()


        instrucciones_procesador_uniprot_json = self.add_search_id_to_json(self.get_json_from_route('Processors_JSONs/uniprot.json'),"FANCA")



        return workflow_result