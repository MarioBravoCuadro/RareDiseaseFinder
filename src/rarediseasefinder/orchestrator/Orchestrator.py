from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.BaseWorkflowStep import BaseWorkflowStep
from src.rarediseasefinder.orchestrator.Workflows.Workflow import Workflow


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
        for workflow in lista:
            print(f"\033[32m Orchestrator initialized with workflows: {workflow.name}\033[0m")
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
                return workflow.check_if_all_steps_available()
        return False

    def get_minium_methods_for_step_from_workflow(self, step_name: str, workflow_name: str) -> dict | None:
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
                return workflow.optional_methods_by_step[step_name]
        return None

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
                return workflow.get_filters_from_method(step_name, method_name)
        return {}

    ########################Stage 2 methods#######################

    def set_selected_optional_method(self, selected_optional_method: str, workflow_step_name: str,
                                     workflow_name: str) -> None:
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
                workflow.set_selected_optional_methods(selected_optional_method, workflow_step_name)

    def set_filter_to_method(self, filters: dict, method_name: str, workflow_step_name: str,
                             workflow_name: str) -> None:
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
                workflow.set_filter_to_method(workflow_step_name, method_name, filters)

    def set_workflow_search_param(self, search_term: str, workflow_name: str) -> None:
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
                workflow.search_param = search_term

    ########################Stage 3 methods#######################

    def start_workflow(self, workflow_name: str) -> None:
        """
        Execute the workflow matching the given name.

        Args:
            workflow_name (str): The name of the workflow to start.

        Returns:
            None
        """
        for workflow in self.workflows_list:
            if workflow_name == workflow.name:
                workflow.steps_execution()

    ########################Debugin methods#######################
    def get_search_param(self, workflow_name: str) -> str | None:
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

    orchestrator.start_workflow("Workflow for TFG")

    print(orchestrator.get_method_filters("df_omim", "Pharos", "Workflow for TFG"))
    orchestrator.set_workflow_search_param("FANCA", "Workflow for TFG")
    print(orchestrator.get_search_param("Workflow for TFG"))

    print("All step available? " + str(orchestrator.get_if_all_steps_available("Workflow for TFG")))

    print(orchestrator.get_minium_methods_for_step_from_workflow("Pharos_Step", "Workflow for TFG"))
    print(orchestrator.get_optional_methods_from_workflow("Pharos_Step", "Workflow for TFG"))

    orchestrator.set_filter_to_method(
            {
                "PRIORIDAD_CLASES": {
                    "Tclin": 1,
                    "Tchem": 2,
                    "Tbio": 3,
                    "Tdark": 4
                },
                "PRIORIDAD_PROPIEDADES": {
                    "p_wrong": 1,
                    "p_ni": 2
                }
            }
        , "df_omim", "Pharos", "Workflow for TFG")

    print("Filtros " + str(orchestrator.get_method_filters("metodo_no_existente", "Pharos", "Workflow for TFG")))
    print("Filtros " + str(orchestrator.get_method_filters("df_omim", "Pharos", "Workflow for TFG")))

    print(orchestrator.get_step("Pharos", "Workflow for TFG").get_filters().get_json_str())

    orchestrator.set_selected_optional_method("metodo_anadido_desde_front", "Pharos", "Workflow for TFG")

    print(orchestrator.get_step("Pharos", "Workflow for TFG").get_filters().get_json_str())
