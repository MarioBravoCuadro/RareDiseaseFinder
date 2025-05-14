import json
from traceback import print_tb

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.OpentargetsWorkflowStep import OpentargetsWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.EnsemblWorkflowStep import EnsemblerWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PantherdbWorkflowStep import PantherdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PharosWorkflowStep import PharosWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep
from src.rarediseasefinder.core.BaseFilter import BaseFilter
from src.rarediseasefinder.orchestrator.WorkflowSteps.StringdbWorkflowStep import StringdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.UniprotWorkflowStep import UniprotWorkflowStep


class Workflow(IWorkflow):
    def __init__(self):
        self.name = "Workflow for TFG"
        self.description = "Fetches x data from Pharos API x data from selleckchem"
        self.listOfSteps = []

        self.add_step_to_list_of_steps({"Pharos": PharosWorkflowStep})
        self.add_step_to_list_of_steps({"Selleckchem": SelleckchemWorkflowStep})
        self.add_step_to_list_of_steps({"Ensembl": EnsemblerWorkflowStep})
        self.add_step_to_list_of_steps({"Opentargets": OpentargetsWorkflowStep})
        self.add_step_to_list_of_steps({"Panther": PantherdbWorkflowStep})
        self.add_step_to_list_of_steps({"Uniprot": UniprotWorkflowStep})
        self.add_step_to_list_of_steps({"Stringdb": StringdbWorkflowStep})

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

        self.minium_methods_uniprot=[
            {
                "METHOD_ID": "function",
                "METHOD_PARSER_FILTERS": ""
            }
            ,
            {
                "METHOD_ID": "subcellular_location",
                "METHOD_PARSER_FILTERS": ""
            }
            ,
            {
                "METHOD_ID": "go_terms",
                "METHOD_PARSER_FILTERS": ""
            }
            ,
            {
                "METHOD_ID": "disease",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "disease_publications",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "parse_variants",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "parse_interactions",
                "METHOD_PARSER_FILTERS": ""
            }
        ]
        self.minium_methods_selleckchem=[
            {
                "METHOD_ID": "obtener_link_selleckchem",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "obtener_links_selleckchem",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "Funcion que da error",
                "METHOD_PARSER_FILTERS": ""
            }
        ]
        self.minium_methods_ensembl=[
            {
                "METHOD_ID": "ensembl_id",
                "METHOD_PARSER_FILTERS": ""
            }
        ]
        self.minium_methods_opentargets=[
            {
                "METHOD_ID": "basic_info",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "pathways",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "known_drugs",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "associated_diseases",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "interactions",
                "METHOD_PARSER_FILTERS": ""
            },
            {
                "METHOD_ID": "mouse_phenotypes",
                "METHOD_PARSER_FILTERS": ""
            }
        ]
        self.minium_methods_pantherdb=[
            {
                "METHOD_ID": "annotation_name",
                "METHOD_PARSER_FILTERS": {}
            }
        ]
        self.minium_methods_stringdb=[
            {
                "METHOD_ID": "get_annotation",
                "METHOD_PARSER_FILTERS": {}
            }
        ]
        self.minium_methods_pharos = [
            {
                "METHOD_ID": "df_info",
                "METHOD_PARSER_FILTERS": {}
            },
            {
                "METHOD_ID": "df_omim",
                "METHOD_PARSER_FILTERS": {}
            },
            {
                "METHOD_ID": "create_protein_protein_relations_df",
                "METHOD_PARSER_FILTERS":self.filtros_parser_pharos_front[0]
            },
            {
                "METHOD_ID": "df_vias",
                "METHOD_PARSER_FILTERS": {}
            },
            {
                "METHOD_ID": "df_numero_vias_por_fuente",
                "METHOD_PARSER_FILTERS": {}
            }
        ]

    def step_pipeline(self):
        #Crear Filtro es un BaseFilter
        pharos_filters = BaseFilter(self.minium_methods_pharos,"PharosProcessor")

        #Añadir termino de busqueda al filtro
        pharos_filters.add_client_search_params("FANCA")

        #Añadir parser method
        pharos_filters.add_parser_method("secuenciasADN",self.filtros_parser_pharos_front)

        #traer el filtro formato json comom string
        pharos_filters_json_string = pharos_filters.get_json_str()

        print(pharos_filters_json_string)
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