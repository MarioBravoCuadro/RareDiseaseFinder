from typing import Any, Type

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.Workflows.Workflow import Workflow
from src.rarediseasefinder.orchestrator.api import workflows, workflow_step


class Orchestrator:

    server = None
    workflows = []
    active_workflow = None

    def __init__(self):
        self.workflows.append(Workflow()) #Añadimos primer workflow.

    def get_workflows(self):
        list_of_workflows=[]
        for workflow in self.workflows:
            list_of_workflows.append(
                {"name":workflow.name, "status": workflow.check_if_all_steps_available()}
            )
        return list_of_workflows

    def start_workflow(self,workflow_name:str):
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                     workflow.steps_execution()

    def get_if_all_steps_available(self, workflow_name:str):
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                    return workflow.check_if_all_steps_available()

    def get_steps(self, workflow:IWorkflow):
        return workflow.get_steps()


    def get_workflow(self,workflow_name :str) -> Type[IWorkflow] | None:
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                    return workflow
        return None

    def get_search_param(self,workflow_name :str) -> Type[IWorkflow] | None:
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                    return workflow.search_param
        return None

    def get_minium_methods_for_step_from_workflow(self, step_name: str, workflow_name: str):
        for workflow in self.workflows:
            if workflow_name ==  workflow.name:
                if workflow.workflow_state == "stage_2":
                    return workflow.minium_methods_by_step[step_name]
        return None

    def get_optional_methods_from_workflow(self, step_name: str, workflow_name: str):
        for workflow in self.workflows:
            if workflow_name ==  workflow.name:
                if workflow.workflow_state == "stage_2":
                    return workflow.optional_methods_by_step[step_name]
        return None

    def get_step_status(self, step_name: str, workflow_name: str):
        for workflow in self.workflows:
            if workflow_name ==  workflow.name:
                if workflow.workflow_state == "stage_2":
                    return workflow.get_step(step_name)
        return None

    def set_active_workflow(self,workflow_name:str):
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                    self.active_workflow == workflow

    def set_workflow_search_term(self, search_term:str, workflow_name:str):
        #añade en el workflow el termino de busqueda introducido en la barra de busqueda
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                     workflow.search_param = search_term

    def set_selected_optional_methods(self,selected_optional_methods,workflow_step_name:str,workflow_name):
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                    workflow.set_selected_optional_methods(workflow_step_name,selected_optional_methods)

    def set_filter_to_method(self,filters,method_name,workflow_step_name:str,workflow_name):
        for workflow in self.workflows:
            if workflow_name == workflow.name:
                if workflow.workflow_state == "stage_2":
                    workflow.set_filter_to_method(workflow_step_name,method_name,filters)

if __name__ == "__main__":
    orchestrator = Orchestrator()

    print(orchestrator.get_workflows())

    orchestrator.start_workflow("Workflow for TFG")


    orchestrator.set_workflow_search_term("FANCA","Workflow for TFG")
    print(orchestrator.get_search_param("Workflow for TFG"))

    print(orchestrator.get_if_all_steps_available("Workflow for TFG"))

    print(orchestrator.get_minium_methods_for_step_from_workflow("Pharos_Step_2","Workflow for TFG"))
    print(orchestrator.get_optional_methods_from_workflow("Pharos_Step_2","Workflow for TFG"))