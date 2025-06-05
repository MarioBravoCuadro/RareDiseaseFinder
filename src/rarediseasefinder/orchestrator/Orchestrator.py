from typing import Any

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.Workflows.Workflow import Workflow
from src.rarediseasefinder.orchestrator.api import workflows


class Orchestrator:

    server = None
    workflows = [IWorkflow]


    def __init__(self):
        self.workflows.append(Workflow()) #Añadimos primer workflow.


    def start_workflow(self,workflow_name:str):
        for workflow in self.workflows:
            if workflow_name in workflow.name:
                workflow.steps_execution()

    def get_if_all_steps_available(self, workflow:IWorkflow):
        return workflow.check_if_all_steps_available()

    def get_steps(self, workflow:IWorkflow):
        return workflow.get_steps()

    def decode_search_params(self,searchConfigFilter):
        pass

    def get_workflows(self):
        list_of_workflows=[]
        for workflow in self.workflows:
            list_of_workflows.append(
                {"name":workflow.name, "status": workflow.check_if_all_steps_available()}
            )
        return list_of_workflows

    def get_workflow(self,workflow_name :str) -> IWorkflow | None:
        for workflow in self.workflows:
            if workflow_name in workflow.name:
                return workflow
        return None

    def set_workflow_search_term(self, search_term:str, workflow_name:str):
        #añade en el workflow el termino de busqueda introducido en la barra de busqueda
        for workflow in self.workflows:
            if workflow_name in workflow.name:
                workflow.search_param = search_term
    def get_minium_methods_for_step_from_workflow(self, step_name: str, workflow_name: str):
        for workflow in self.workflows:
            if workflow_name in workflow.name:
                if hasattr(workflow, 'minimum_methods_by_step'):
                    return workflow.minimum_methods_by_step.get(step_name, [])
        return []
      def get_optional_methods_from_workflow(self, workflow:IWorkflow):
        if hasattr(workflow, 'optional_methods'):
            return workflow.optional_methods
        return workflow._generate_optional_methods()

    def update_selected_optional_methods(self, list_of_methods):
        pass
