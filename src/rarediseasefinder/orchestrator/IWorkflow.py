from abc import abstractmethod, ABC

from src.rarediseasefinder.core.BaseFilter import BaseFilter
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
    def listOfSteps(self):
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
    def check_if_all_steps_available(self):
        """Abstract method to be implemented by subclasses to check if all their defined steps are available."""
        pass

    def instantiate_steps(self):
        """
        Instantiates step objects within self.listOfSteps if they are stored as types.

        Assumes self.listOfSteps is a list of dictionaries, where dictionary values
        can be step types (classes) that need to be instantiated.
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

    def check_if_all_steps_available(self):
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

    def add_step_to_list_of_steps(self, step:[str,IWorkflowStep]):
        """
        Adds a new step to the workflow's list of steps.

        Assumes self.listOfSteps is an attribute that is a list.

        Args:
            step: The step to add to self.listOfSteps. Typically a dictionary
                  representing the step or its configuration.
        """
        self.listOfSteps.append(step)

    def get_step(self, step_name: str) -> IWorkflowStep | None:
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

    def generate_optional_methods(self):
        """
        Genera los métodos opcionales calculando la diferencia entre method_map y minimum_methods
        para cada step del workflow. Maneja múltiples steps que apuntan al mismo procesador.
        
        Returns:
            dict: Diccionario con métodos opcionales por step
        """
        optional_methods = {}
        
        # Iterar sobre las claves de minimum_methods_by_step para manejar cada configuración
        for step_key, step_config in self.minium_methods_by_step.items():
            step_name = step_config.get("step_name", "")
            processor = step_config.get("processor", "")
            minimum_methods = step_config.get("methods", [])
            minimum_method_ids = {method["METHOD_ID"] for method in minimum_methods}
            
            # Buscar el step instance correspondiente en listOfSteps
            step_instance = None
            for step_dict in self.listOfSteps:
                if step_name in step_dict:
                    step_instance = step_dict[step_name]
                    break
            
            if step_instance is None:
                print(f"\033[33mWarning: No se encontró step instance para {step_name}\033[0m")
                continue
                
            # Obtener todos los métodos disponibles del step
            all_methods = step_instance.get_method_map()
            all_method_ids = set(all_methods.keys())
            
            # Calcular métodos opcionales (diferencia entre todos los métodos y los mínimos)
            optional_method_ids = all_method_ids - minimum_method_ids
            #print(f"\033[31mOptional methods for {step_key} ({step_name}): {optional_method_ids}\033[0m")
            
            # Crear estructura de métodos opcionales para cada step_key único
            if optional_method_ids:  # Solo si hay métodos opcionales
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
                # Incluso si no hay métodos opcionales, crear la estructura vacía
                optional_methods[step_key] = {
                    "step_name": step_name,
                    "processor": processor,
                    "methods": []
                }
                
        return optional_methods


    def set_filter_to_method(self,filters,method_name,workflow_step_name):
        for step in self.listOfSteps:
            if step.keys == workflow_step_name:
                step[workflow_step_name].get_filters().set_filter_to_method(filters,method_name)


