from ..IWorkflow import IWorkflow

from ..WorkflowSteps.PharmGKBWorkflowStep import PharmGKBWorkflowStep
from ..WorkflowSteps.OpentargetsWorkflowStep import OpentargetsWorkflowStep
from ..WorkflowSteps.EnsemblWorkflowStep import EnsemblWorkflowStep
from ..WorkflowSteps.PPIAtlasWorkflowStep import PPIAtlasWorkflowStep
from ..WorkflowSteps.PantherdbWorkflowStep import PantherdbWorkflowStep
from ..WorkflowSteps.PharmacologyWorkflowStep import PharmacologyWorkflowStep
from ..WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep
from ..WorkflowSteps.DrugCentralWorkflowStep import DrugCentralWorkflowStep
from ..WorkflowSteps.StringdbWorkflowStep import StringdbWorkflowStep
from ..WorkflowSteps.UniprotWorkflowStep import UniprotWorkflowStep

from ...core.BaseFilter import BaseFilter
from ...core.constants import get_standard_external_links, NO_DATA_MARKER

from..Workflows.DataframesUtils import DataframesUtils
from ..Workflows.JSONFactory import JSONFactory


class NoPharosWorkflow(IWorkflow):
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

        self.json_factory = JSONFactory()
        self.workflow_state = "stage_1"
        self._search_param = ""
        self._name = "NoPharosWorkflow"
        self._description = "Workflow con secciones SIN PHAROS; DESCRIPCIÓN,PROCESOS,PATHWAYS,INTERACCIONES,ENFERMEDADES,TERAPÉUTICA,REFERENCIAS."
        self._listOfSteps = []

        self.add_step_to_list_of_steps({"Uniprot": UniprotWorkflowStep})
        self.add_step_to_list_of_steps({"Ensembl": EnsemblWorkflowStep})
        self.add_step_to_list_of_steps({"Panther": PantherdbWorkflowStep})
        self.add_step_to_list_of_steps({"Opentargets": OpentargetsWorkflowStep})
        self.add_step_to_list_of_steps({"Stringdb": StringdbWorkflowStep})
        self.add_step_to_list_of_steps({"Selleckchem": SelleckchemWorkflowStep})
        self.add_step_to_list_of_steps({"DrugCentral": DrugCentralWorkflowStep})
        self.add_step_to_list_of_steps({"Pharmacology": PharmacologyWorkflowStep})
        self.add_step_to_list_of_steps({"Pharmgkb": PharmGKBWorkflowStep})
        self.add_step_to_list_of_steps({"PPIAtlas": PPIAtlasWorkflowStep})

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
                        "METHOD_ID": "interactions",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "external_links",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "function_references",
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
                    },
                    {
                        "METHOD_ID": "external_links",
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
                    },
                    {
                        "METHOD_ID": "pathways",
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
            },
            "Selleckchem_Step": {
                "step_name": "Selleckchem",
                "processor": "SelleckchemProcessor",
                "methods": [
                    {
                        "METHOD_ID": "obtener_links_selleckchem",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "DrugCentral_Step": {
                "step_name": "DrugCentral",
                "processor": "DrugCentralProcessor",
                "methods": [
                    {
                        "METHOD_ID": "drug_results",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "Pharmacology_Step": {
                "step_name": "Pharmacology",
                "processor": "PharmacologyProcessor",
                "methods": [
                    {
                        "METHOD_ID": "target_id",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "comments",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "references",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "interactions",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "Pharmgkb_Step": {
                "step_name": "Pharmgkb",
                "processor": "PharmGKBProcessor",
                "methods": [
                    {
                        "METHOD_ID": "gene_symbols",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "label_annotations",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "literature",
                        "METHOD_PARSER_FILTERS": ""
                    },
                    {
                        "METHOD_ID": "pathways",
                        "METHOD_PARSER_FILTERS": ""
                    }
                ]
            },
            "PPIAtlas_Step": {
                "step_name": "PPIAtlas",
                "processor": "PPIAtlasProcessor",
                "methods": [
                    {
                        "METHOD_ID": "ppi_table",
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
        ensembl_filters = BaseFilter(self._minium_methods_by_step["Ensembl_Step"]["methods"], "EnsemblProcessor")
        pantherdb_filters = BaseFilter(self._minium_methods_by_step["Panther_Step"]["methods"], "PantherProcessor")
        opentargets_filters = BaseFilter(self._minium_methods_by_step["Opentargets_Step"]["methods"],"OpenTargetsProcessor")
        stringdb_filters = BaseFilter(self._minium_methods_by_step["Stringdb_Step"]["methods"], "StringDbProcessor")
        selleckchem_filters = BaseFilter(self._minium_methods_by_step["Selleckchem_Step"]["methods"], "SelleckchemProcessor")
        drugcentral_filters = BaseFilter(self._minium_methods_by_step["DrugCentral_Step"]["methods"], "DrugCentralProcessor")
        pharmgkb_filters = BaseFilter(self._minium_methods_by_step["Pharmgkb_Step"]["methods"], "PharmGKBProcessor")
        pharmacology_filters = BaseFilter(self._minium_methods_by_step["Pharmacology_Step"]["methods"], "PharmacologyProcessor")
        ppiatlas_filters = BaseFilter(self._minium_methods_by_step["PPIAtlas_Step"]["methods"], "PPIAtlasProcessor")

        # Coger step de la lista de pasos

        uniprot_step = self.get_step("Uniprot")
        ensembl_step = self.get_step("Ensembl")
        pantherdb_step = self.get_step("Panther")
        opentargets_step = self.get_step("Opentargets")
        stringdb_step = self.get_step("Stringdb")
        selleckchem_step = self.get_step("Selleckchem")
        drugcentral_step = self.get_step("DrugCentral")
        pharmgkb_step = self.get_step("Pharmgkb")
        pharmacology_step = self.get_step("Pharmacology")
        ppiatlas_step = self.get_step("PPIAtlas")

        # Añadir filtro a cada step

        uniprot_step.set_filters(uniprot_filters)
        ensembl_step.set_filters(ensembl_filters)
        pantherdb_step.set_filters(pantherdb_filters)
        opentargets_step.set_filters(opentargets_filters)
        stringdb_step.set_filters(stringdb_filters)
        selleckchem_step.set_filters(selleckchem_filters)
        drugcentral_step.set_filters(drugcentral_filters)
        pharmgkb_step.set_filters(pharmgkb_filters)
        pharmacology_step.set_filters(pharmacology_filters)
        ppiatlas_step.set_filters(ppiatlas_filters)



    def stage_2_pipeline(self):
        #Cambios desde el front clase simbólica, no modificar.
        self.workflow_state = "stage_2"

    def stage_3_pipeline(self):
        #Ejecución del pipeline.
        self.workflow_state = "stage_3"

        # Coger step de la lista de pasos
        uniprot_step = self.get_step("Uniprot")
        ensembl_step = self.get_step("Ensembl")
        pantherdb_step = self.get_step("Panther")
        drugcentral_step = self.get_step("DrugCentral")

        #Coger los filtros
        uniprot_filters =  uniprot_step.get_filters()
        ensembl_filters =  ensembl_step.get_filters()
        pantherdb_filters =  pantherdb_step.get_filters()
        drugcentral_filters = drugcentral_step.get_filters()

        #Añadir parametro de búsqueda
        uniprot_filters.add_client_search_params(self._search_param)
        ensembl_filters.add_client_search_params(self._search_param)
        pantherdb_filters.add_client_search_params(self._search_param)
        drugcentral_filters.add_client_search_params(self._search_param)
        #Ejecutar cada step
        uniprot_result = uniprot_step.process()
        ensembl_result = ensembl_step.process()
        panther_result = pantherdb_step.process()
        drugcentral_result = drugcentral_step.process()

        print(uniprot_result.keys())
        print(ensembl_result.keys())
        print(panther_result.keys())
        print(drugcentral_result.keys())
        print("ensembl_id: " + ensembl_result["ensembl_id"].iloc[0][0])
        opentargets_step = self.get_step("Opentargets")
        opentargets_filters = opentargets_step.get_filters()
        #Accedemos al ensembl_id que se necesita como entrada en opentargets.
        opentargets_filters.add_client_search_params(ensembl_result["ensembl_id"].iloc[0][0])
        opentargets_result = opentargets_step.process()

        print(opentargets_result.keys())

        # Procesar los resultados de OpenTargets para StringDB
        # Aquí asumimos que opentargets_result["interactions"]["Proteína interactuante"] contiene los nombres de las proteínas
        # y opentargets_result["interactions"]["Puntuación"] contiene las puntuaciones
        stringdb_results = []
        for prot, puntuacion in zip(opentargets_result["interactions"]["Proteína interactuante"], opentargets_result["interactions"]["Puntuación"]):
            stringdb_step = self.get_step("Stringdb")
            stringdb_filters = stringdb_step.get_filters()
            stringdb_filters.add_client_search_params(prot)
            results = stringdb_step.process()
            results["get_annotation"]["Puntuación"] = puntuacion
            stringdb_results.append(results["get_annotation"])

        stringdb_results = DataframesUtils.create_dataframe(stringdb_results)
        opentargets_result["interactions"] = stringdb_results
        print(opentargets_result["interactions"].keys())
        #print(stringdb_results)

        # Procesar los resultados de OpenTargets para Selleckchem
        # Aquí asumimos que opentargets_result["known_drugs"]["Nombre"] contiene los nombres de los fármacos
        # y que queremos obtener el enlace de Selleckchem para cada uno.
        # Inicializar una lista para almacenar los resultados de Selleckchem
        # Coger step de la lista de pasos Selleckchem
        # Iterar sobre los nombres de los fármacos y buscar en Selleckchem
        selleckchem_and_drugcentral_results = []
        print("DrugCentral: " + str(drugcentral_result["drug_results"].shape[0]) + " resultados")
        for row_dict in drugcentral_result["drug_results"].to_dict(orient="records"):
            if "DrugName" in row_dict:
                drug = row_dict["DrugName"]
                print("Buscando en Selleckchem: " + drug)

                selleckchem_step = self.get_step("Selleckchem")
                selleckchem_filters = selleckchem_step.get_filters()
                selleckchem_filters.add_client_search_params(drug)
                results_s = selleckchem_step.process()

                if results_s and not NO_DATA_MARKER in results_s["obtener_links_selleckchem"]:
                    row_dict["Link Selleckchem"] = results_s["obtener_links_selleckchem"].iloc[0, 0]
                    selleckchem_and_drugcentral_results.append(row_dict)

        selleckchem_and_drugcentral_results = DataframesUtils.create_dataframe(selleckchem_and_drugcentral_results)
        selleckchem_and_drugcentral_results = DataframesUtils.expand_comma_separated_column(
            selleckchem_and_drugcentral_results,
            "Link Selleckchem"
        )
        print(selleckchem_and_drugcentral_results)

        drugcentral_result["drug_results"] = selleckchem_and_drugcentral_results

        # Coger step de la lista de pasos
        pharmacology_step = self.get_step("Pharmacology")
        # Coger los filtros
        pharmacology_filters = pharmacology_step.get_filters()
        # Añadir parámetro de búsqueda
        pharmacology_filters.add_client_search_params(self._search_param)
        pharmacology_result = pharmacology_step.process()

        print(pharmacology_result.keys())

        # Coger step de la lista de pasos
        pharmgkb_step = self.get_step("Pharmgkb")
        # Coger los filtros
        pharmgkb_filters = pharmgkb_step.get_filters()
        # Añadir parámetro de búsqueda
        pharmgkb_filters.add_client_search_params(self._search_param)
        pharmgkb_result = pharmgkb_step.process()
        print(pharmgkb_result.keys())

        # Coger step de la lista de pasos
        ppiatlas_step = self.get_step("PPIAtlas")
        # Coger los filtros
        ppiatlas_filters = ppiatlas_step.get_filters()
        # Añadir parámetro de búsqueda
        ppiatlas_filters.add_client_search_params(self._search_param)
        ppiatlas_result = ppiatlas_step.process()
        print(ppiatlas_result.keys())

        result = self._create_json(self._search_param, 
                                   uniprot_result, 
                                   ppiatlas_result, 
                                   opentargets_result, 
                                   panther_result, 
                                   None, 
                                   pharmgkb_result, 
                                   pharmacology_result, 
                                   drugcentral_result,
                                   ensembl_result)

        return result


    def steps_execution(self)-> dict:
      return self.stage_3_pipeline()

    def _create_json(self,
                     search_term="",
                     uniprot_result=None,
                     ppiatlas_result=None,
                     opentargets_result=None,
                     panther_result=None,
                     pharos_result=None,
                     pharmgkb_result=None,
                     guide_to_pharmacology_result=None,
                     drugcentral_result=None,
                     ensembl_result=None) -> dict:
        """
        Crea una estructura JSON estandarizada a partir de los dataframes específicos.

        Args:
            uniprot_result: Resultados de Uniprot
            ppiatlas_result: Resultados de PPIAtlas
            stringdb_results: Resultados de StringDB
            pharos_result: Resultados de Pharos
            selleckchem_result: Resultados de Selleckchem

        Returns:
            dict: Estructura JSON con los resultados organizados
        """



        self.json_factory.set_search_term(search_term)
        self.json_factory.set_date()

        # ----- SECCIÓN: DESCRIPCIÓN -----
        # Función molecular de UniProt

        self.json_factory.add_content(
            section="DESCRIPCIÓN",
            title="UniProt: Función molecular",
            display="table",
            data=DataframesUtils.dataframe_to_dict(uniprot_result["function"])
        )
        self.json_factory.add_content(
            section="DESCRIPCIÓN",
            title="UniProt: Referencias de la función molecular",
            display="sheet",
            data=DataframesUtils.dataframe_to_dict(uniprot_result["function_references"])
        )

        # Localización subcelular de UniProt
        self.json_factory.add_content(
            section="DESCRIPCIÓN",
            title="UniProt: Localización subcelular",
            display="sheet",
            data=DataframesUtils.dataframe_to_dict(uniprot_result["subcellular_location"])
        )
        # ----- SECCIÓN: PROCESOS -----
        self.json_factory.add_content(
            section="PROCESOS",
            title="Panther: Procesos",
            display="table",
            data=DataframesUtils.dataframe_to_dict(panther_result["annotations"])
        )
        # ----- SECCIÓN: PATHWAYS -----
        self.json_factory.add_content(
            section="PATHWAYS",
            title="Panther: Pathways",
            display="table",
            data=DataframesUtils.dataframe_to_dict(panther_result["pathways"])
        )
        self.json_factory.add_content(
            section="PATHWAYS",
            title="OpenTargets: Pathways",
            display="table",
            data=DataframesUtils.dataframe_to_dict(opentargets_result["pathways"])
        )

        # ----- SECCIÓN: INTERACCIONES -----
        self.json_factory.add_content(
            section="INTERACCIONES",
            title="OpenTargets + StringDB: Interacciones proteína-proteína",
            display="table",
            data=DataframesUtils.dataframe_to_dict(opentargets_result["interactions"])
        )
        self.json_factory.add_content(
            section="INTERACCIONES",
            title="UniProt: Interacciones proteína-proteína",
            display="table",
            data=DataframesUtils.dataframe_to_dict(uniprot_result["interactions"])
        )
        self.json_factory.add_content(
            section="INTERACCIONES",
            title="PPI Atlas: Interacciones proteína-proteína",
            display="table",
            data=DataframesUtils.dataframe_to_dict(ppiatlas_result["ppi_table"])
        )
        self.json_factory.add_content(
            section="INTERACCIONES",
            title="PharmGKB: Genes asociados",
            display="table",
            data=DataframesUtils.dataframe_to_dict(pharmgkb_result["gene_symbols"])
        )
        # ----- SECCIÓN: ENFERMEDADES -----
        # Enfermedades de UniProt
        self.json_factory.add_content(
            section="ENFERMEDADES",
            title="UniProt: Enfermedades asociadas",
            display="table",
            data=DataframesUtils.dataframe_to_dict(uniprot_result["disease"])
        )

        self.json_factory.add_content(
            section="ENFERMEDADES",
            title="OpenTargets: Enfermedades asociadas",
            display="table",
            data=DataframesUtils.dataframe_to_dict(opentargets_result["associated_diseases"])
        )

        # ----- SECCIÓN: TERAPÉUTICA -----
        self.json_factory.add_content(
            section="TERAPÉUTICA",
            title="OpenTargets: Fármacos conocidos",
            display="table",
            data=DataframesUtils.dataframe_to_dict(opentargets_result["known_drugs"])
        )
        self.json_factory.add_content(
            section="TERAPÉUTICA",
            title="DrugCentral + Selleckchem: Resultados de fármacos",
            display="table",
            data=DataframesUtils.dataframe_to_dict(drugcentral_result["drug_results"])
        )
        self.json_factory.add_content(
            section="TERAPÉUTICA",
            title="PharmGKB: Label Annotations",
            display="table",
            data=DataframesUtils.dataframe_to_dict(pharmgkb_result["label_annotations"])
        )

        self.json_factory.add_content(
            section="TERAPÉUTICA",
            title="GuideToFarmacology: Link",
            display="table",
            data=DataframesUtils.dataframe_to_dict(guide_to_pharmacology_result["target_id"])
        )
        self.json_factory.add_content(
            section="TERAPÉUTICA",
            title="GuideToFarmacology: Comentarios",
            display="table",
            data=DataframesUtils.dataframe_to_dict(guide_to_pharmacology_result["comments"])
        )
        # ----- SECCIÓN: REFERENCIAS -----
        self.json_factory.add_content(
            section="REFERENCIAS",
            title="UniProt: Publicaciones por enfermedad",
            display="table",
            data=DataframesUtils.dataframe_to_dict(uniprot_result["disease_publications"])
        )
        self.json_factory.add_content(
            section="REFERENCIAS",
            title="PharmGKB: Literatura asociada",
            display="table",
            data=DataframesUtils.dataframe_to_dict(pharmgkb_result["literature"])
        )
        self.json_factory.add_content(
            section="REFERENCIAS",
            title="GuideToFarmacology: Referencias",
            display="table",
            data=DataframesUtils.dataframe_to_dict(guide_to_pharmacology_result["references"])
        )
        self.json_factory.add_content(
            section="REFERENCIAS",
            title="GuideToFarmacology: Interacciones",
            display="table",
            data=DataframesUtils.dataframe_to_dict(guide_to_pharmacology_result["interactions"])
        )
         # ----- SECCIÓN: ENLACES EXTERNOS -----
        self.json_factory.add_content(
            section="ENLACES EXTERNOS",
            title="Fuentes variadas: Enlaces Externos",
            display="table",
            data=get_standard_external_links(self._search_param)
        )
        self.json_factory.add_content(
            section="ENLACES EXTERNOS",
            title="Uniprot: Enlaces Externos",
            display="table",
            data=DataframesUtils.dataframe_to_dict(uniprot_result["external_links"])
        )
        self.json_factory.add_content(
            section="ENLACES EXTERNOS",
            title="Ensembl: Enlaces Externos",
            display="table",
            data=DataframesUtils.dataframe_to_dict(ensembl_result["external_links"])
        )
        # Obtener el JSON resultante
        return self.json_factory.get_json()

if __name__ == "__main__":
    workflow = NoPharosWorkflow()
    workflow._search_param = "TTR"

    print(workflow.steps_execution())
