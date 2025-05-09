import json

from src.rarediseasefinder.biodata_providers.pharos.PharosProcessor import PharosProcessor
from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.PharosWorkflowStep import PharosWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep
from src.rarediseasefinder.orchestrator.BaseFilter import BaseFilter


class Workflow(IWorkflow):
    name = None
    description = None
    listOfSteps=None

    def __init__(self):
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


    minium_methods_uniprot=''
    minium_methods_selleckchem=''
    minium_methods_ensembl=''

    filtros_parser_pharos_front = {
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

    minium_methods_pharos = [
        {
            "METHOD_ID": "create_protein_protein_relations_df",
            "METHOD_PARSER_FILTERS": filtros_parser_pharos_front
        }
    ]

    def steps_execution(self)-> list[dict]:
        #Crear Filtro es un BaseFilter
        pharos_filters = BaseFilter(self.minium_methods_pharos,"PharosProcessor")
        #Añadir termino de busqueda al filtro
        pharos_filters.add_client_search_params("FANCA")

        #Añadir parser method
        pharos_filters.add_parser_method("secuenciasADN","")

        #traer el filtro formato json comom string
        pharos_filters_json_string = pharos_filters.get_json_str()
        #convertir el str a objeto json (objeto != archivo)
        pharos_filters_json_object = json.loads(pharos_filters_json_string)

        pharos_step = PharosWorkflowStep(pharos_filters_json_object)
        status_code = pharos_step.get_status_code()
        result = pharos_step.process()

        return result


if __name__ == "__main__":
    Workflow().steps_execution()