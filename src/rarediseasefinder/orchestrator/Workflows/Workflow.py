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
        selleck_chem_filters = BaseFilter(self.minium_methods_selleckchem,"SelleckchemProcessor")
        ensembler_filters = BaseFilter(self.minium_methods_ensembl,"EnsemblProcessor")
        opentargets_filters = BaseFilter(self.minium_methods_opentargets,"OpenTargetsProcessor")
        pantherdb_filters = BaseFilter(self.minium_methods_pantherdb,"PantherdbProcessor")
        uniprot_filters = BaseFilter(self.minium_methods_uniprot,"UniprotProcessor")
        stringdb_filters = BaseFilter(self.minium_methods_stringdb,"StringdbProcessor")


        #traer el filtro formato json comom string
        pharos_filters_json_string = pharos_filters.get_json_str()
        selleck_chem_filters_json_string = selleck_chem_filters.get_json_str()
        ensembler_filters_json_string = ensembler_filters.get_json_str()
        opentargets_filters_json_string = opentargets_filters.get_json_str()
        pantherdb_filters_json_string = pantherdb_filters.get_json_str()
        uniprot_filters_json_string = uniprot_filters.get_json_str()
        stringdb_filters_json_string = stringdb_filters.get_json_str()

        #convertir el str a objeto json (objeto != archivo)
        pharos_filters_json_object = json.loads(pharos_filters_json_string)
        selleck_chem_filters_json_object = json.loads(selleck_chem_filters_json_string)
        ensembler_filters_json_object = json.loads(ensembler_filters_json_string)
        opentargets_filters_json_object = json.loads(opentargets_filters_json_string)
        pantherdb_filters_json_object = json.loads(pantherdb_filters_json_string)
        uniprot_filters_json_object = json.loads(uniprot_filters_json_string)
        stringdb_filters_json_object = json.loads(stringdb_filters_json_string)

        #Añadir termino de busqueda al filtro
        #Sacalos del main.py  filters_json los terminos de busqueda
        pharos_filters.add_client_search_params("FANCA")
        selleck_chem_filters.add_client_search_params("TCL")
        ensembler_filters.add_client_search_params("FANCA")
        opentargets_filters.add_client_search_params("ENSG00000118271")
        pantherdb_filters.add_client_search_params("P02766")
        uniprot_filters.add_client_search_params("O15360")
        stringdb_filters.add_client_search_params("ENSP00000360522")


        #Coger step de la lista de pasos
        pharos_step = self.get_step("Pharos")
        selleckchem_step = self.get_step("Selleckchem")
        ensembler_step = self.get_step("Ensembl")
        opentargets_step = self.get_step("Opentargets")
        pantherdb_step = self.get_step("Panther")
        uniprot_step = self.get_step("Uniprot")
        stringdb_step = self.get_step("Stringdb")
        
        #Añadir filtro a cada step
        pharos_step.set_filters(pharos_filters_json_object)
        selleckchem_step.set_filters(selleck_chem_filters_json_object)
        ensembler_step.set_filters(ensembler_filters_json_object)
        opentargets_step.set_filters(opentargets_filters_json_object)
        pantherdb_step.set_filters(pantherdb_filters_json_object)
        uniprot_step.set_filters(uniprot_filters_json_object)
        stringdb_step.set_filters(stringdb_filters_json_object)

        #Ejecutar cada step
        pharos_status_code = pharos_step.get_status_code()
        selleckchem_status_code = selleckchem_step.get_status_code()
        ensembler_status_code = ensembler_step.get_status_code()
        opentargets_status_code = opentargets_step.get_status_code()
        pantherdb_status_code = pantherdb_step.get_status_code()
        uniprot_status_code = uniprot_step.get_status_code()
        stringdb_status_code = stringdb_step.get_status_code()

        #Ejecutar cada step
        pharos_result = pharos_step.process()
        selleckchem_result = selleckchem_step.process()
        ensembler_result = ensembler_step.process()
        opentargets_result = opentargets_step.process()
        pantherdb_result = pantherdb_step.process()
        uniprot_result = uniprot_step.process()
        stringdb_result = stringdb_step.process()

        return [pharos_result, selleckchem_result, ensembler_result, opentargets_result, pantherdb_result, uniprot_result, stringdb_result]

    def steps_execution(self)-> list[dict]:
        return self.step_pipeline()

if __name__ == "__main__":
    print (Workflow().check_if_all_steps_available())
    print(Workflow().steps_execution())




"""
Example:
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
"""