from abc import abstractmethod, ABC


from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.BaseWorkflowStep import BaseWorkflowStep


class IWorkflow(ABC):
    @property
    @abstractmethod
    def workflow_state(self):
        pass

    @workflow_state.setter
    @abstractmethod
    def workflow_state(self, value: str):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def listOfSteps(self)->list:
        pass

    @listOfSteps.setter
    @abstractmethod
    def listOfSteps(self, value: list):
        pass

    @property
    @abstractmethod
    def search_param(self):
        pass

    @search_param.setter
    @abstractmethod
    def search_param(self, value: str):
        pass

    @property
    @abstractmethod
    def minium_methods_by_step(self) -> dict:
        pass

    @minium_methods_by_step.setter
    @abstractmethod
    def minium_methods_by_step(self, value: dict):
        pass

    @property
    @abstractmethod
    def optional_methods_by_step(self) -> dict:
        pass

    @optional_methods_by_step.setter
    @abstractmethod
    def optional_methods_by_step(self, value: dict):
        pass

    @abstractmethod
    def get_steps(self):
        """Abstract method to be implemented by subclasses to define or return their workflow steps.
            Example content of the dict: {"Pharos" : PharosWorkflowStep} :str and :IWorkflowStep"""

        pass

    @abstractmethod
    def check_if_all_steps_available(self)->bool:
        """Abstract method to be implemented by subclasses to check if all their defined steps are available."""
        pass

    @abstractmethod
    def steps_execution(self):
        pass

    def instantiate_steps(self) -> None:
        """
        Instantiates step objects within self.listOfSteps if they are stored as types (classes).

        Assumes self.listOfSteps is a list of dictionaries, where dictionary values
        can be step types (classes) that need to be instantiated.
        
        Returns:
            None
        """
        for step in self.listOfSteps:
            for key, step_instance in step.items():
                if isinstance(step_instance, type):
                    step[key] = step_instance()

    def get_steps(self) -> list[dict]:
        """
        Returns the list of steps associated with the workflow.

        Assumes self.listOfSteps is an attribute containing a list of dictionaries,
        where each dictionary represents a step or a collection of named steps.

        Example content of the dict: {"Pharos": PharosWorkflowStep}

        Returns:
            list[dict]: The list of steps.
        """
        return self.listOfSteps

    def check_if_all_steps_available(self) -> bool:
        """
        Checks if all instantiated steps in self.listOfSteps have a status code of 200.

        Assumes self.listOfSteps is a list of dictionaries, where each dictionary
        contains step instances that have a get_status_code() method.

        Returns:
            bool: True if all steps are available (status code 200), False otherwise.
        """
        for step in self.listOfSteps:
            for step_instance in step.values():
                if step_instance.get_status_code() != 200:
                    return False
        return True

    def add_step_to_list_of_steps(self, step: dict) -> None:
        """
        Adds a new step to the workflow's list of steps.

        Assumes self.listOfSteps is an attribute that is a list.

        Args:
            step (dict[str, IWorkflowStep]): The step to add to self.listOfSteps. 
                                           Typically, a dictionary representing the step or its configuration.
                                           Format: {"step_name": step_instance}
        
        Returns:
            None
        """
        self.listOfSteps.append(step)

    def get_step(self, step_name: str) -> BaseWorkflowStep | None:
        """
        Retrieves a specific step by its name from the workflow's list of steps.

        Searches through self.listOfSteps, where each item is assumed to be a
        dictionary mapping step names to step instances.

        Args:
            step_name (str): The name of the step to retrieve.

        Returns:
            The step instance if found, otherwise None.
        """
        for step in self.listOfSteps:
            if step_name in step:
                return step[step_name]
        return None

    def generate_optional_methods(self) -> dict:
        """
        Generates optional methods by calculating the difference between method_map and minimum_methods
        for each workflow step. Handles multiple steps pointing to the same processor.
        
        This method iterates over all steps defined in minium_methods_by_step and calculates
        which methods are available in each processor but are not defined as minimum methods.
        
        Returns:
            dict: Dictionary with optional methods per step. The structure is:
                  {
                      "step_key": {
                          "step_name": str,
                          "processor": str,
                          "methods": [
                              {
                                  "METHOD_ID": str,
                                  "METHOD_PARSER_FILTERS": dict
                              }, ...
                          ]
                      }, ...
                  }
        """
        optional_methods = {}
        
        # Iterate over minimum_methods_by_step keys to handle each configuration
        for step_key, step_config in self.minium_methods_by_step.items():
            step_name = step_config.get("step_name", "")
            processor = step_config.get("processor", "")
            minimum_methods = step_config.get("methods", [])
            minimum_method_ids = {method["METHOD_ID"] for method in minimum_methods}
            
            # Find the corresponding step instance in listOfSteps
            step_instance = None
            for step_dict in self.listOfSteps:
                if step_name in step_dict:
                    step_instance = step_dict[step_name]
                    break
            
            if step_instance is None:
                print(f"\033[33mWarning: Step instance not found for {step_name}\033[0m")
                continue
                
            # Get all available methods from the step
            all_methods = step_instance.get_method_map()
            all_method_ids = set(all_methods.keys())
            
            # Calculate optional methods (difference between all methods and minimum ones)
            optional_method_ids = all_method_ids - minimum_method_ids
            #print(f"\033[31mOptional methods for {step_key} ({step_name}): {optional_method_ids}\033[0m")
            
            # Create optional methods structure for each unique step_key
            if optional_method_ids:  # Only if there are optional methods
                optional_methods[step_key] = {
                    "step_name": step_name,
                    "processor": processor,
                    "methods": [
                        {
                            "METHOD_ID": method_id,
                            "METHOD_PARSER_FILTERS": {}
                        }
                        for method_id in optional_method_ids
                    ]
                }
            else:
                # Even if there are no optional methods, create empty structure
                optional_methods[step_key] = {
                    "step_name": step_name,
                    "processor": processor,
                    "methods": []
                }
                
        return optional_methods

    def get_filters_from_method(self, workflow_step_name: str, method_name: str) -> dict:
        """
        Retrieves filters for a specific method within a workflow step.
        
        Searches for the specified step in the list of steps and returns the filters
        for the indicated method within that step.
        
        Args:
            workflow_step_name (str): Name of the workflow step where the method is located
            method_name (str): Name of the method to get filters from
            
        Returns:
            dict: The filters for the specified method, or empty dict if not found
        """
        for step in self.listOfSteps:
            if list(step.keys())[0] == workflow_step_name:
               return  step[workflow_step_name].get_filters().get_filters_from_method(method_name)
        return {}

    def set_filter_to_method(self,workflow_step_name: str, method_name: str, filters: dict) -> None:
        """
        Sets specific filters for a method within a workflow step.
        
        Searches for the specified step in the list of steps and applies the provided
        filters to the indicated method within that step.
        
        Args:
            filters (dict): Dictionary with filters to apply to the method
            method_name (str): Name of the method to which filters will be applied
            workflow_step_name (str): Name of the workflow step where the method is located
            
        Returns:
            None
        """
        for step in self.listOfSteps:
            if list(step.keys())[0] == workflow_step_name:
                step[workflow_step_name].get_filters().set_filter_to_method(filters, method_name)

    def set_selected_optional_methods(self, selected_optional_method: str, workflow_step_name: str) -> None:
        """
        Sets a selected optional parser method to a specific workflow step.

        Args:
            selected_optional_method (str): ID of the optional method to select.
            workflow_step_name (str): Name of the workflow step to apply the optional method.

        Returns:
            None
        """
        for step in self.listOfSteps:
            if list(step.keys())[0] == workflow_step_name:
                step[workflow_step_name].get_filters().add_parser_method(selected_optional_method, {})  #Filtros vacios porque se añade primero el método opcional y luego se seleccionan filtros para este.

