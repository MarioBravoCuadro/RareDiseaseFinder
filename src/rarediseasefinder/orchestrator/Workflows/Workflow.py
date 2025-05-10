import json

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.PharosWorkflowStep import PharosWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep
from src.rarediseasefinder.orchestrator.BaseFilter import BaseFilter


class Workflow(IWorkflow):
    def __init__(self):
        self.name = "Workflow for TFG"
        self.description = "Fetches x data from Pharos API x data from selleckchem"
        self.listOfSteps = []

        self.add_step_to_list_of_steps({"Pharos": PharosWorkflowStep})
        self.add_step_to_list_of_steps({"Selleckchem": SelleckchemWorkflowStep})
        self.instantiate_steps()

        self.filtros_parser_pharos_front = [
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
        ]

        self.minium_methods_uniprot=[]
        self.minium_methods_selleckchem=[]
        self.minium_methods_ensembl=[]
        self.minium_methods_pharos = [
            {
                "METHOD_ID": "create_protein_protein_relations_df",
                "METHOD_PARSER_FILTERS": self.filtros_parser_pharos_front[0]
            },
            {
                "METHOD_ID": "create_protein_protein_relations_df",
                "METHOD_PARSER_FILTERS": self.filtros_parser_pharos_front[0]
            }
        ]


    def instantiate_steps(self):
        for step in self.listOfSteps:
            for key, step_instance in step.items():
                if isinstance(step_instance, type):
                    step[key] = step_instance()

    def get_steps(self)-> list[dict]:
        return self.listOfSteps

    def check_if_all_steps_available(self):
        for step in self.listOfSteps:
            for step_instance in step.values():
                if step_instance.get_status_code() != 200:
                    return False
        return True

    def add_step_to_list_of_steps(self, step):
        self.listOfSteps.append(step)

    def get_step(self, step_name: str):
        for step in self.listOfSteps:
            if step_name in step:
                return step[step_name]
        return None

    def step_pipeline(self):
        #Crear Filtro es un BaseFilter
        pharos_filters = BaseFilter(self.minium_methods_pharos,"PharosProcessor")

        #Añadir termino de busqueda al filtro
        pharos_filters.add_client_search_params("FANCA")

        #Añadir parser method
        pharos_filters.add_parser_method("secuenciasADN",self.filtros_parser_pharos_front)

        #traer el filtro formato json comom string
        pharos_filters_json_string = pharos_filters.get_json_str()

        #convertir el str a objeto json (objeto != archivo)
        pharos_filters_json_object = json.loads(pharos_filters_json_string)

        pharos_step = self.get_step("Pharos")

        pharos_step.set_filters(pharos_filters_json_object)
        status_code = pharos_step.get_status_code()
        result = pharos_step.process()

        return result

    def steps_execution(self)-> list[dict]:
        return self.step_pipeline()

if __name__ == "__main__":
    print (Workflow().check_if_all_steps_available())
    print(Workflow().steps_execution())