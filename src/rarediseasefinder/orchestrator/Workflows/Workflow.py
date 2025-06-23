import json
from abc import ABC
from typing import List

from pandas.core.interchange.dataframe_protocol import DataFrame

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.OpentargetsWorkflowStep import OpentargetsWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.EnsemblWorkflowStep import EnsemblerWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PantherdbWorkflowStep import PantherdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PharosWorkflowStep import PharosWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep
from src.rarediseasefinder.core.BaseFilter import BaseFilter
from src.rarediseasefinder.orchestrator.WorkflowSteps.StringdbWorkflowStep import StringdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.UniprotWorkflowStep import UniprotWorkflowStep
from src.rarediseasefinder.orchestrator.Workflows.DataframesUtils import DataframesUtils


class Workflow(IWorkflow):
    @property
    def workflow_state(self):
        return self._workflow_state

    @workflow_state.setter
    def workflow_state(self, value: str):
        self._workflow_state = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def listOfSteps(self):
        return self._listOfSteps

    @listOfSteps.setter
    def listOfSteps(self, value: list):
        self._listOfSteps = value

    @property
    def search_param(self):
        return self._search_param

    @search_param.setter
    def search_param(self, value: str):
        self._search_param = value

    @property
    def minium_methods_by_step(self)-> dict:
        return self._minium_methods_by_step

    @minium_methods_by_step.setter
    def minium_methods_by_step(self, value: dict):
        self._minium_methods_by_step = value

    @property
    def optional_methods_by_step(self)-> dict:
        return self._optional_methods_by_step

    @optional_methods_by_step.setter
    def optional_methods_by_step(self, value: dict):
        self._optional_methods_by_step = value

    def __init__(self):

        self.workflow_state = "stage_1"
        self._search_param = ""
        self._name = "WorkflowTFG"
        self._description = "Fetches x data from Pharos API x data from selleckchem"
        self._listOfSteps = []


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

        self._minium_methods_by_step = {
            "Uniprot_Step": {
                "step_name": "Uniprot",
                "processor": "UniprotProcessor",
                "methods": [
                    {
                        "METHOD_ID": "function",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "subcellular_location",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "go_terms",
                        "METHOD_PARSER_FILTERS": ""
                    },
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
            },
            "Selleckchem_Step": {
                "step_name": "Selleckchem",
                "processor": "SelleckchemProcessor",
                "methods": [
                    {
                        "METHOD_ID": "obtener_link_selleckchem",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "obtener_links_selleckchem",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "Ensembl_Step": {
                "step_name": "Ensembl",
                "processor": "EnsemblProcessor",
                "methods": [
                    {
                        "METHOD_ID": "ensembl_id",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "Opentargets_Step": {
                "step_name": "Opentargets",
                "processor": "OpenTargetsProcessor",
                "methods": [
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
            },
            "Panther_Step": {
                "step_name": "Panther",
                "processor": "PantherProcessor",
                "methods": [
                    {
                        "METHOD_ID": "panther_class",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "Stringdb_Step": {
                "step_name": "Stringdb",
                "processor": "StringDbProcessor",
                "methods": [
                    {
                        "METHOD_ID": "get_annotation",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "Pharos_Step": {
                "step_name": "Pharos",
                "processor": "PharosProcessor",
                "methods": [
                    {
                        "METHOD_ID": "df_info",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "df_omim",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "create_protein_protein_relations_df",
                        "METHOD_PARSER_FILTERS":  self.filtros_parser_pharos_front[0]
                    },
                    {
                        "METHOD_ID": "df_vias",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "df_numero_vias_por_fuente",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            }
        }

        # Generar métodos opcionales dinámicamente
        self._optional_methods_by_step = self.generate_optional_methods()

        self.stage_1_pipeline()


    def stage_1_pipeline(self):
        self.workflow_state = "stage_1"

    def stage_2_pipeline(self):
        #Cambios desde el front clase simbólica, no modificar.
        self.workflow_state = "stage_2"

    def stage_3_pipeline(self):
        #Ejecución del pipeline

        # Añadir filtros inciales
        pharos_filters = BaseFilter(self._minium_methods_by_step["Pharos_Step"]["methods"], "PharosProcessor")
        selleck_chem_filters = BaseFilter(self._minium_methods_by_step["Selleckchem_Step"]["methods"],
                                          "SelleckchemProcessor")
        ensembler_filters = BaseFilter(self._minium_methods_by_step["Ensembl_Step"]["methods"], "EnsemblProcessor")
        opentargets_filters = BaseFilter(self._minium_methods_by_step["Opentargets_Step"]["methods"],
                                         "OpenTargetsProcessor")
        pantherdb_filters = BaseFilter(self._minium_methods_by_step["Panther_Step"]["methods"], "PantherProcessor")
        uniprot_filters = BaseFilter(self._minium_methods_by_step["Uniprot_Step"]["methods"], "UniprotProcessor")
        stringdb_filters = BaseFilter(self._minium_methods_by_step["Stringdb_Step"]["methods"], "StringDbProcessor")

        pharos_filters.add_client_search_params(self._search_param)
        selleck_chem_filters.add_client_search_params("TCL")
        ensembler_filters.add_client_search_params(self._search_param)
        opentargets_filters.add_client_search_params("ENSG00000118271")
        pantherdb_filters.add_client_search_params("P02766")
        uniprot_filters.add_client_search_params("O15360")
        stringdb_filters.add_client_search_params("ENSP00000360522")

        #  pharos_filters.set_filter_to_method("", "")

        # Coger step de la lista de pasos
        pharos_step = self.get_step("Pharos")
        selleckchem_step = self.get_step("Selleckchem")
        ensembler_step = self.get_step("Ensembl")
        opentargets_step = self.get_step("Opentargets")
        pantherdb_step = self.get_step("Panther")
        uniprot_step = self.get_step("Uniprot")
        stringdb_step = self.get_step("Stringdb")

        # Añadir filtro a cada step
        pharos_step.set_filters(pharos_filters)
        selleckchem_step.set_filters(selleck_chem_filters)
        ensembler_step.set_filters(ensembler_filters)
        opentargets_step.set_filters(opentargets_filters)
        pantherdb_step.set_filters(pantherdb_filters)
        uniprot_step.set_filters(uniprot_filters)
        stringdb_step.set_filters(stringdb_filters)


        self.workflow_state = "stage_3"

        print(pharos_step.get_filters().json_filter)

        #Ejecutar cada step
        pharos_result = pharos_step.process()
        #selleckchem_result = selleckchem_step.process()
        ensembler_result = ensembler_step.process()
        opentargets_result = opentargets_step.process()
        pantherdb_result = pantherdb_step.process()
        uniprot_result = uniprot_step.process()
        stringdb_result = stringdb_step.process()

        self.workflow_state = "stage_1"

        results = [
            ("pharos", pharos_result),
            ("ensembl", ensembler_result),
            ("opentargets", opentargets_result),
            ("panther", pantherdb_result),
            ("uniprot", uniprot_result),
            ("stringdb", stringdb_result)
        ]
        output = []
        for idx, (fuente, res) in enumerate(results, 1):
            output.append({
                "indice": idx,
                "fuente": fuente,
                "resultado": DataframesUtils.dataframe_to_json(res)
            })
        return output


    def steps_execution(self)-> list[dict]:
      return self.stage_3_pipeline()
