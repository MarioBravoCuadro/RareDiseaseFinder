from typing import List, Dict, Any
import logging
import pandas as pd

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.BaseWorkflowStep import BaseWorkflowStep
from src.rarediseasefinder.orchestrator.Workflows.Workflow import Workflow
from src.rarediseasefinder.core.errors import IncorrectStageError

class Orchestrator:
    server = None
    workflows_list = []

    def __init__(self, lista: list[IWorkflow]):
        """
        Initialize the Orchestrator and register workflows.

        Args:
            lista (list[IWorkflow]): List of workflow instances to register.

        Returns:
            None
        """
        print(f"\033[34mx-x-x-x-x-x-x-x Orchestrator initializing x-x-x-x-x-x-x-x")
        for workflow in lista:
            print(f"\033[32m Orchestrator initialized with workflow: {workflow.name}\033[0m")

            #incializamos los estados de los workflows a stage_1
            workflow.workflow_state = "stage_1"
            print(f"El estado del workflow {workflow.name} se ha incializado en {workflow.workflow_state}")

        self.workflows_list = lista

    ########################Stage 1 methods#######################

    def get_workflows(self) -> list[dict]:
        """
        Retrieve the list of available workflows with their status.

        Returns:
            list[dict]: A list of workflow summaries, each containing 'name' and 'status'.
                       Format: [{"name": str, "status": bool}, ...]
        """
        list_of_workflows = []
        for workflow in self.workflows_list:
            if workflow.workflow_state != "stage_1":
                raise IncorrectStageError(workflow.workflow_state, "stage_1", f"get_workflows")
            list_of_workflows.append(
                {"name": workflow.name, "status": workflow.check_if_all_steps_available()}
            )
        return list_of_workflows

    def get_if_all_steps_available(self, workflow_name: str) -> bool:
        """
        Check if all steps in the specified workflow are available.

        Args:
            workflow_name (str): The name of the workflow to check.

        Returns:
            bool: True if all steps are available, False otherwise.
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_1":
                    raise IncorrectStageError(workflow.workflow_state, "stage_1", f"get_if_all_steps_available para workflow '{workflow_name}'")
                return workflow.check_if_all_steps_available()
        return False

    def get_minium_methods_for_step_from_workflow(self, step_name: str, workflow_name: str) -> dict | None :
        """
        Get the JSON of minimum methods for a given step in a workflow.

        Args:
            step_name (str): The step key to query.
            workflow_name (str): The workflow containing the step.

        Returns:
            dict | None: The minimum methods configuration, or None if not found.

        Note:
            Returns for a workflow step the JSON of minimum methods, e.g.:
            {'step_name': 'Pharos', 'processor': 'PharosProcessor', 'methods': [{'METHOD_ID': 'Metodo prueba', 'METHOD_PARSER_FILTERS': {}}]}
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_1":
                    raise IncorrectStageError(workflow.workflow_state, "stage_1", f"get_workflows")
                return workflow.minium_methods_by_step[step_name]
        return None

    def get_optional_methods_from_workflow(self, step_name: str, workflow_name: str) -> dict | None:
        """
        Get the JSON of optional methods for a given step in a workflow.

        Args:
            step_name (str): The step key to query.
            workflow_name (str): The workflow containing the step.

        Returns:
            dict | None: The optional methods configuration, or None if not found.

        Note:
            Returns for a workflow step the JSON of optional methods, e.g.:
            {'step_name': 'Pharos', 'processor': 'PharosProcessor', 'methods': [{'METHOD_ID': 'Metodo prueba', 'METHOD_PARSER_FILTERS': {}}]}
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_1":
                    raise IncorrectStageError(workflow.workflow_state, "stage_1", f"get_optional_methods_from_workflow")
                return workflow.optional_methods_by_step[step_name]
        return None

    def get_list_of_steps_names(self, workflow_name: str) -> list[str] | dict[Any, Any]:
        """
        Retrieve all steps from a specific workflow.
        
        Args:
            workflow_name (str): The name of the workflow.
            
        Returns:
            dict: Dictionary of steps with step names as keys and IWorkflowStep instances as values.
                 Example: {"Pharos": PharosWorkflowStep, "UniProt": UniProtWorkflowStep}
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_1":
                    raise IncorrectStageError(workflow.workflow_state, "stage_1", f"get_list_of_steps_names")
                return workflow.get_list_of_steps_names()
        return {}

    def get_method_filters(self, method_name: str, step_name: str, workflow_name: str) -> dict:
        """
        Retrieve filters for a specific method in a workflow step.
        
        Args:
            method_name (str): The name of the method to get filters from.
            step_name (str): The name of the workflow step.
            workflow_name (str): The name of the workflow.
            
        Returns:
            dict: The filters for the specified method, or empty dict if not found.
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_1":
                    raise IncorrectStageError(workflow.workflow_state, "stage_1", f"get_method_filters")
                return workflow.get_filters_from_method(step_name, method_name)
        return {}

    def set_stage_2(self,workflow_name) -> None :
         for workflow in self.workflows_list:
             if workflow_name == workflow_name:
                 if workflow.workflow_state != "stage_1":
                     raise IncorrectStageError(workflow.workflow_state, "stage_1", f"set_stage_2 para workflow '{workflow_name}'")
                 workflow.workflow_state = "stage_2"

    ########################Stage 2 methods#######################

    def set_selected_optional_method(self, selected_optional_method: str, workflow_step_name: str,
                                     workflow_name: str) -> None :
        """
        Apply a selected optional parser method to a workflow step.

        Args:
            selected_optional_method (str): The method ID to apply.
            workflow_step_name (str): The step where to apply the method.
            workflow_name (str): The name of the workflow.

        Returns:
            None

        Note:
            Adds the selected optional method to a step of the workflow.
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_2":
                    raise IncorrectStageError(workflow.workflow_state, "stage_2", f"set_selected_optional_method")
                workflow.set_selected_optional_methods(selected_optional_method, workflow_step_name)

    def set_filter_to_method(self, filters: dict, method_name: str, workflow_step_name: str,
                             workflow_name: str) -> None :
        """
        Apply filter configuration to a specific method in a workflow step.

        Args:
            filters (dict): The filter settings to apply.
            method_name (str): The method to filter.
            workflow_step_name (str): The step containing the method.
            workflow_name (str): The name of the workflow.

        Returns:
            None

        Note:
            Adds the selected filter to a method of a workflow step.
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_2":
                    raise IncorrectStageError(workflow.workflow_state, "stage_2", f"set_filter_to_method")
                workflow.set_filter_to_method(workflow_step_name, method_name, filters)

    def set_workflow_search_param(self, search_term: str, workflow_name: str) -> None :
        """
        Set the search parameter for a specific workflow.

        Args:
            search_term (str): The term to set.
            workflow_name (str): The workflow in which to set the term.

        Returns:
            None

        Note:
            Adds the search term entered on the search box to the workflow.
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_2":
                    raise IncorrectStageError(workflow.workflow_state, "stage_2", f"set_workflow_search_param")
                workflow.search_param = search_term

    def set_stage_3(self,workflow_name):
         for workflow in self.workflows_list:
             if workflow_name == workflow_name:
                 if workflow.workflow_state != "stage_2":
                     raise IncorrectStageError(workflow.workflow_state, "stage_2", f"set_stage_3 para workflow '{workflow_name}'")
                 workflow.workflow_state = "stage_3"

    ########################Stage 3 methods#######################

    def start_workflow(self, workflow_name: str):
        """
        Execute the workflow matching the given name.

        Args:
            workflow_name (str): The name of the workflow to start.

        Returns:
            list[dict]
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                if workflow.workflow_state != "stage_3":
                    raise IncorrectStageError(workflow.workflow_state, "stage_3", f"start_workflow")
                return  workflow.steps_execution()

    def set_stage_1(self,workflow_name):
         for workflow in self.workflows_list:
             if workflow_name == workflow.name:
                 print(f"Workflow '{workflow_name}' está actualmente en stage: {workflow.workflow_state}")
                 print(f"Intentando cambiar workflow '{workflow_name}' a stage_1")
                 if workflow.workflow_state != "stage_3":
                     raise IncorrectStageError(workflow.workflow_state, "stage_3", f"set_stage_1 para workflow '{workflow_name}'")
                 workflow.workflow_state = "stage_1"
                 print(f"Workflow '{workflow_name}' cambiado exitosamente a stage_1")

    ########################Debugin methods#######################
    def get_search_param(self, workflow_name: str) -> str | None :
        """
        Retrieve the search parameter for the specified workflow.

        Args:
            workflow_name (str): The name of the workflow.

        Returns:
            str | None: The current search parameter, or None if not set.

        Note:
            Returns the term entered the search box for the workflow.
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                return workflow.search_param
        return None

    def get_step(self, step_name: str, workflow_name: str) -> BaseWorkflowStep | None:
        """
        Retrieve the BaseWorkflowStep instance for debugging purposes.

        Args:
            step_name (str): The name of the step to retrieve.
            workflow_name (str): The workflow in which to search.

        Returns:
            BaseWorkflowStep | None: The step instance, or None if not found.

        Note:
            This method returns the BaseWorkflowStep object for backend debugging.
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                return workflow.get_step(step_name)
        return None


if __name__ == "__main__":
    wokflows = [Workflow()]
    orchestrator = Orchestrator(wokflows)


    print(orchestrator.get_workflows())
    print(orchestrator.get_list_of_steps_names("WorkflowTFG"))
    print(orchestrator.get_minium_methods_for_step_from_workflow("Pharos_Step","WorkflowTFG"))
    print(orchestrator.get_optional_methods_from_workflow("Pharos_Step","WorkflowTFG"))

    print("All step available? " + str(orchestrator.get_if_all_steps_available("WorkflowTFG")))

    print(orchestrator.get_minium_methods_for_step_from_workflow("Pharos_Step", "Workflow for TFG"))
    print(orchestrator.get_optional_methods_from_workflow("Pharos_Step", "Workflow for TFG"))

    orchestrator.set_stage_2("WorkflowTFG")

    orchestrator.set_workflow_search_param("FANCA","WorkflowTFG")
    orchestrator.set_stage_3("WorkflowTFG")
    print( orchestrator.start_workflow("WorkflowTFG"))
