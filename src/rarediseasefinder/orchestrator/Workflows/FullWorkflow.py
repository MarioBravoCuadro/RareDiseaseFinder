import json
from abc import ABC
from typing import List

from IPython.core.release import description
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


class FullWorkflow(IWorkflow):
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
        self._name = "FullWorkflow"
        self._description = "Workflow con secciones; DESCRIPCIÓN,PROCESOS (Funcionoma),PATHWAYS,INTERACCIONES,ENFERMEDADES,TERAPÉUTICA,REFERENCIAS."
        self._listOfSteps = []

        self.add_step_to_list_of_steps({"Uniprot": UniprotWorkflowStep})
        self.add_step_to_list_of_steps({"Ensembl": EnsemblerWorkflowStep})
        self.add_step_to_list_of_steps({"Panther": PantherdbWorkflowStep})
        self.add_step_to_list_of_steps({"Opentargets": OpentargetsWorkflowStep})
        self.add_step_to_list_of_steps({"Stringdb": StringdbWorkflowStep})


        self.instantiate_steps()

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
                        "METHOD_ID": "parse_interactions",
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
            "Panther_Step": {
                "step_name": "Panther",
                "processor": "PantherProcessor",
                "methods": [
                    {
                        "METHOD_ID": "annotations",
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
            "Stringdb_Step": {
                "step_name": "Stringdb",
                "processor": "StringDbProcessor",
                "methods": [
                    {
                        "METHOD_ID": "get_annotation",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            }
        }

        # Generar métodos opcionales dinámicamente
        self._optional_methods_by_step = self.generate_optional_methods()

        self.stage_1_pipeline()


    def stage_1_pipeline(self):
        #Inicializar los filtros default modificables por el usuario.
        self.workflow_state = "stage_1"

        # Añadir filtros inciales
        uniprot_filters = BaseFilter(self._minium_methods_by_step["Uniprot_Step"]["methods"], "UniprotProcessor")
        ensembler_filters = BaseFilter(self._minium_methods_by_step["Ensembl_Step"]["methods"], "EnsemblProcessor")
        pantherdb_filters = BaseFilter(self._minium_methods_by_step["Panther_Step"]["methods"], "PantherProcessor")
        opentargets_filters = BaseFilter(self._minium_methods_by_step["Opentargets_Step"]["methods"],"OpenTargetsProcessor")
        stringdb_filters = BaseFilter(self._minium_methods_by_step["Stringdb_Step"]["methods"], "StringDbProcessor")

        # Coger step de la lista de pasos

        uniprot_step = self.get_step("Uniprot")
        ensembler_step = self.get_step("Ensembl")
        pantherdb_step = self.get_step("Panther")
        opentargets_step = self.get_step("Opentargets")
        stringdb_step = self.get_step("Stringdb")



        # Añadir filtro a cada step

        uniprot_step.set_filters(uniprot_filters)
        ensembler_step.set_filters(ensembler_filters)
        pantherdb_step.set_filters(pantherdb_filters)
        opentargets_step.set_filters(opentargets_filters)
        stringdb_step.set_filters(stringdb_filters)



    def stage_2_pipeline(self):
        #Cambios desde el front clase simbólica, no modificar.
        self.workflow_state = "stage_2"

    def stage_3_pipeline(self):
        #Ejecución del pipeline.
        self.workflow_state = "stage_3"

        # Coger step de la lista de pasos
        uniprot_step = self.get_step("Uniprot")
        ensembler_step = self.get_step("Ensembl")
        pantherdb_step = self.get_step("Panther")

        #Coger los filtros
        uniprot_filters =  uniprot_step.get_filters()
        ensembler_filters =  ensembler_step.get_filters()
        pantherdb_filters =  pantherdb_step.get_filters()

        #Añadir parametro de búsqueda
        uniprot_filters.add_client_search_params(self._search_param)
        ensembler_filters.add_client_search_params(self._search_param)
        pantherdb_filters.add_client_search_params(self._search_param)

        #Ejecutar cada step
        uniprot_result = uniprot_step.process()
        ensembler_result = ensembler_step.process()
        panther_result = pantherdb_step.process()

        print(uniprot_result.keys())
        print(ensembler_result.keys())
        print(panther_result.keys())
        print("ensembl_id: " + ensembler_result["ensembl_id"].iloc[0][0])

        opentargets_step = self.get_step("Opentargets")
        opentargets_filters = opentargets_step.get_filters()
        #Accedemos al ensembl_id que se necesita como entrada en opentargets.
        opentargets_filters.add_client_search_params(ensembler_result["ensembl_id"].iloc[0][0])
        opentargets_result = opentargets_step.process()

        print(opentargets_result.keys())


        #Llamadas a stringdb con id sacado de opentarget
        stringdb_results = []
        print("Interacciones:" +opentargets_result["interactions"])
        for prot, puntuacion in zip(opentargets_result["interactions"], opentargets_result["interactions"]["puntuaciones"]):
            stringdb_step = self.get_step("Stringdb")
            stringdb_filters = stringdb_step.get_filters()
            stringdb_filters.add_client_search_params(prot)
            results = stringdb_step.process()
            # Añadir puntuación
            if isinstance(results, dict):
                results["Puntuación"] = puntuacion
            else:
                results = {"result": results, "Puntuación": puntuacion}
            stringdb_results.append(results)

        stringdb_results = DataframesUtils.create_dataframe(stringdb_results)
        print(stringdb_results.to_string())
        stringdb_results.keys()





        """
                results = [
                    {
                        "Section":"Descripcion",
                        "Data":[
                            {
                             "Fuente": "Uniprot",
                             "df_info" : uniprot_result["function"]
                            },
                            {
                                "Fuente": "Uniprot",
                                "df_info": uniprot_result["subcellular_location"]
                            },
                            {
                                "Fuente": "Pharos",
                                "df_info": pharos_result["df_info"]
                            }
        
                        ]
                    },
                    {
                        "Section": "PATHWAYS",
                        "Data": [
                            {
                                "Fuente": "Pharos",
                                "df_info": pharos_result["df_vias"]
                            }
                        ]
                    },
                    {
                        "Section": "INTERACCIONES",
                        "Data": [
                            {
                                "Fuente": "Pharos",
                                "df_info": pharos_result["create_protein_protein_relations_df"]
                            }
                        ]
                    },
                    {
                        "Section": "ENFERMEDADES",
                        "Data": [
                            {
                                "Fuente": "Uniprot",
                                "df_info": uniprot_result["disease"]
                            },
                            {
                                "Fuente": "Pharos",
                                "df_info": pharos_result["df_info"]
                            }
                        ]
                    },
                    {
                        "Section": "TERAPÉUTICA",
                        "Data": [
                            {
                                "Fuente": "Selleckchem",
                                "df_info": selleckchem_result["obtener_links_selleckchem"]
                            }
                        ]
                    },
                    {
                        "Section": "REFERENCIAS",
                        "Data": [
                            {
                                "Fuente": "Uniprot",
                                "df_info": uniprot_result["disease_publications"]
                            }
                        ]
                    },
                    {
                        "Section": "Opcionales",
                        "Data": [
                            {
                                "Fuente": "Uniprot",
                                "df_info": uniprot_result["go_terms"]
                            }
                        ]
                    }
        
                ]
                """


        self.workflow_state = "stage_1"

        return []


    def steps_execution(self)-> list[dict]:
      return self.stage_3_pipeline()

if __name__ == "__main__":
    workflow = FullWorkflow()
    workflow._search_param = "FANCA"

    print(workflow.steps_execution())
