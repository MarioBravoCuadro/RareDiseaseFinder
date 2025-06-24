from typing import Dict, Any, Optional, List
import pandas as pd

from src.rarediseasefinder.orchestrator.Workflows.BaseWorkflow import BaseWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.OpentargetsWorkflowStep import OpentargetsWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.EnsemblWorkflowStep import EnsemblerWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PantherdbWorkflowStep import PantherdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PharosWorkflowStep import PharosWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.StringdbWorkflowStep import StringdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.UniprotWorkflowStep import UniprotWorkflowStep
from src.rarediseasefinder.biodata_providers.ensembl.EnsemblProcessor import EnsemblProcessor
from src.rarediseasefinder.biodata_providers.opentargets.OpenTargetsProcessor import OpenTargetsProcessor
from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor

class FullWorkflow(BaseWorkflow):
    """
    Implementación completa del workflow que integra todas las fuentes de datos.
    Gestiona directamente la resolución de parámetros entre steps.
    """
    
    def __init__(self):
        """
        Inicializa el workflow completo.
        """
        super().__init__(
            name="FullWorkflow", 
            description="Workflow completo con análisis de todas las fuentes de datos bioinformáticas"
        )
    
    def _initialize_steps(self):
        """
        Inicializa todos los steps para este workflow.
        """
        self.add_step_to_list_of_steps({"Pharos": PharosWorkflowStep})
        self.add_step_to_list_of_steps({"Selleckchem": SelleckchemWorkflowStep})
        self.add_step_to_list_of_steps({"Ensembl": EnsemblerWorkflowStep})
        self.add_step_to_list_of_steps({"Opentargets": OpentargetsWorkflowStep})
        self.add_step_to_list_of_steps({"Panther": PantherdbWorkflowStep})
        self.add_step_to_list_of_steps({"Uniprot": UniprotWorkflowStep})
        self.add_step_to_list_of_steps({"Stringdb": StringdbWorkflowStep})
        
        # Instanciar todos los steps
        self.instantiate_steps()
    
    def _configure_minimum_methods(self):
        """
        Configura los métodos mínimos para cada step.
        """
        # Configuración de filtros para Pharos
        self.filtros_parser_pharos = {
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
        
        self._minium_methods_by_step = {
            "Ensembl_Step": {
                "step_name": "Ensembl",
                "processor": "EnsemblProcessor",
                "methods": [
                    {"METHOD_ID": "get_ensembl_id_from_symbol", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "get_symbol_from_ensembl_id", "METHOD_PARSER_FILTERS": ""}
                ]
            },
            "Opentargets_Step": {
                "step_name": "Opentargets",
                "processor": "OpentargetsProcessor",
                "methods": [
                    {"METHOD_ID": "get_target_from_ensembl_id", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "get_disease_from_target", "METHOD_PARSER_FILTERS": ""}
                ]
            },
            "Uniprot_Step": {
                "step_name": "Uniprot",
                "processor": "UniprotProcessor",
                "methods": [
                    {"METHOD_ID": "function", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "subcellular_location", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "disease", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "ecs", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "get_xml_from_id", "METHOD_PARSER_FILTERS": ""}
                ]
            },
            "Panther_Step": {
                "step_name": "Panther",
                "processor": "PantherProcessor",
                "methods": [
                    {"METHOD_ID": "get_go_terms", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "get_pathways", "METHOD_PARSER_FILTERS": ""}
                ]
            },
            "StringDB_Step": {
                "step_name": "Stringdb",
                "processor": "StringdbProcessor",
                "methods": [
                    {"METHOD_ID": "get_interactions", "METHOD_PARSER_FILTERS": ""}
                ]
            },
            "Selleckchem_Step": {
                "step_name": "Selleckchem",
                "processor": "SelleckchemProcessor",
                "methods": [
                    {"METHOD_ID": "obtener_links_selleckchem", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "obtener_link_selleckchem", "METHOD_PARSER_FILTERS": ""}
                ]
            },
            "Pharos_Step": {
                "step_name": "Pharos",
                "processor": "PharosProcessor",
                "methods": [
                    {"METHOD_ID": "df_info", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "df_omim", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "create_protein_protein_relations_df", "METHOD_PARSER_FILTERS": self.filtros_parser_pharos},
                    {"METHOD_ID": "df_vias", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "df_numero_vias_por_fuente", "METHOD_PARSER_FILTERS": ""}
                ]
            }
        }
    
    def _get_execution_order(self) -> List[str]:
        """
        Define el orden específico de ejecución para este workflow,
        respetando las dependencias entre steps.
        
        Returns:
            List[str]: Lista de nombres de steps en orden de ejecución
        """
        # Este orden está diseñado para respetar todas las dependencias
        # Los steps primero en la lista se ejecutan primero
        return [
            "Ensembl",     # Primero (proporciona ID para Opentargets)
            "Opentargets", # Segundo (depende de Ensembl, proporciona datos para Selleckchem)
            "Uniprot",     # Tercero (proporciona ID para StringDB)
            "Panther",     # Cuarto 
            "Stringdb",    # Quinto (depende de Uniprot)
            "Selleckchem", # Sexto (depende de Opentargets)
            "Pharos"       # Séptimo (sin dependencias específicas)
        ]
    
    def _resolve_search_params(self) -> None:
        """
        Resuelve los parámetros de búsqueda para todos los steps.
        Implementa la lógica de dependencias entre steps, transformando
        los parámetros según sea necesario.
        """
        # Valor inicial para todos los steps es el parámetro de búsqueda principal
        # Lo usamos para las fuentes que no tienen dependencias específicas
        self._step_params = {
            "Ensembl": self._search_param,
            "Uniprot": self._search_param,
            "Panther": self._search_param,
            "Pharos": self._search_param
        }
        
        # --- Resolución para Opentargets (depende de Ensembl) ---
        try:
            # Crear un procesador Ensembl temporal para obtener el ID
            ensembl_processor = EnsemblProcessor()
            
            # Usamos el search_param original para consultar Ensembl
            ensembl_data = ensembl_processor.retriever.fetch(self._search_param)
            
            # Extraemos el ID de Ensembl usando el parser
            ensembl_id_df = ensembl_processor.parser.parse_id(ensembl_data)
            
            if not ensembl_id_df.empty:
                # El ID está en el primer índice de la columna 0
                ensembl_id = ensembl_id_df.iloc[0, 0]
                self._step_params["Opentargets"] = ensembl_id
                print(f"ID de Ensembl para Opentargets: {ensembl_id}")
            else:
                print("No se pudo obtener ID de Ensembl para Opentargets")
        except Exception as e:
            print(f"Error al resolver ID de Ensembl para Opentargets: {str(e)}")
        
        # --- Resolución para StringDB (depende de Uniprot) ---
        try:
            # Crear un procesador Uniprot temporal
            uniprot_processor = UniprotProcessor()
            
            # Usamos el search_param original para consultar Uniprot
            uniprot_data = uniprot_processor.retriever.fetch(self._search_param)
            
            # Buscamos el campo "accession" o cualquier otro que contenga el ID para StringDB
            for method_name, method_func in uniprot_processor.method_map.items():
                if method_name == "function":  # El método function suele tener el accession ID
                    result_df = getattr(uniprot_processor.parser, method_func)(uniprot_data)
                    if not result_df.empty and "accession" in result_df.columns:
                        string_id = result_df["accession"].iloc[0]
                        self._step_params["Stringdb"] = string_id
                        print(f"ID de Uniprot para StringDB: {string_id}")
                        break
            
            if "Stringdb" not in self._step_params:
                print("No se pudo obtener ID de Uniprot para StringDB")
        except Exception as e:
            print(f"Error al resolver ID de Uniprot para StringDB: {str(e)}")
        
        # --- Resolución para Selleckchem (depende de Opentargets) ---
        if "Opentargets" in self._step_params:
            try:
                # Crear un procesador OpenTargets temporal
                opentargets_processor = OpenTargetsProcessor()
                
                # Usamos el ID de Ensembl resuelto anteriormente
                opentargets_data = opentargets_processor.retriever.fetch(self._step_params["Opentargets"])
                
                # Buscamos drugs en los resultados
                drug_list = []
                
                # El método get_disease_from_target suele tener la lista de fármacos
                result_df = opentargets_processor.parser.create_known_drugs_df(opentargets_data)
                
                if not result_df.empty and "Nombre" in result_df.columns:
                    drug_list = result_df["Nombre"].tolist()
                
                if drug_list:
                    self._step_params["Selleckchem"] = drug_list
                    print(f"Lista de fármacos para Selleckchem: {drug_list[:3]}...")
                else:
                    print("No se pudo obtener lista de fármacos para Selleckchem")
            except Exception as e:
                print(f"Error al resolver lista de fármacos para Selleckchem: {str(e)}")
        else:
            print("No se puede resolver Selleckchem porque falta Opentargets")
    
    def _get_category_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Define la configuración de categorías para este workflow.
        
        Returns:
            Dict[str, Dict[str, Any]]: Configuración de categorías
        """
        return {
            "1": {
                "title": "Información funcional de la proteína"
            },
            "2": {
                "title": "Patología y enfermedades asociadas"
            },
            "3": {
                "title": "Literatura científica por enfermedad"
            },
            "4": {
                "title": "Interacciones y vías metabólicas"
            },
            "5": {
                "title": "Información genómica"
            },
            "6": {
                "title": "Localización subcelular"
            },
            "7": {
                "title": "Potencial farmacológico"
            }
        }
    
    def _get_method_category_mapping(self) -> Dict[str, str]:
        """
        Define el mapeo entre métodos y categorías para este workflow.
        
        Returns:
            Dict[str, str]: Mapeo de method_id a category_id
        """
        return {
            # Uniprot - diferentes métodos van a diferentes categorías
            "function": "1",
            "subcellular_location": "6",
            "disease": "2",
            "get_xml_from_id": "3",
            "ecs": "4",
            
            # Pharos
            "df_info": "1",
            "df_omim": "2",
            "create_protein_protein_relations_df": "4",
            "df_vias": "4",
            "df_numero_vias_por_fuente": "4",
            
            # Selleckchem
            "obtener_link_selleckchem": "7",
            "obtener_links_selleckchem": "7",
            
            # Ensembl
            "get_ensembl_id_from_symbol": "5",
            "get_symbol_from_ensembl_id": "5",
            
            # OpenTargets
            "get_target_from_ensembl_id": "5",
            "get_disease_from_target": "2",
            
            # Panther
            "get_go_terms": "1",
            "get_pathways": "4",
            
            # StringDB
            "get_interactions": "4"
        }
        
    def _get_grouping_config(self) -> Dict[str, Optional[str]]:
        """
        Define qué métodos requieren agrupación de sus DataFrames y por qué columna.
        
        Returns:
            Dict[str, Optional[str]]: Mapeo de method_id a columna de agrupación
        """
        return {
            # Agrupar enfermedades de Uniprot por nombre
            "disease": "diseaseName",
            
            # Agrupar vías por fuente
            "df_vias": "source",
            
            # Agrupar interacciones por tipo
            "get_interactions": "interactionType",
            
            # Agrupar publicaciones por tipo de enfermedad
            "get_xml_from_id": "disease"
        }