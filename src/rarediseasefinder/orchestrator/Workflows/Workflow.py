from src.rarediseasefinder.orchestrator.Workflows.BaseWorkflow import BaseWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.OpentargetsWorkflowStep import OpentargetsWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.EnsemblWorkflowStep import EnsemblerWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PantherdbWorkflowStep import PantherdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.PharosWorkflowStep import PharosWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.SelleckchemWorkflowStep import SelleckchemWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.StringdbWorkflowStep import StringdbWorkflowStep
from src.rarediseasefinder.orchestrator.WorkflowSteps.UniprotWorkflowStep import UniprotWorkflowStep


class Workflow(BaseWorkflow):
    """
    Implementación de Workflow de ejemplo.
    Define los steps específicos y la configuración de métodos mínimos.
    """
    
    def __init__(self):
        """
        Inicializa el workflow con nombre y descripción específicos.
        """
        super().__init__(
            name="WorkflowTFG", 
            description="Extrae datos de múltiples APIs bioinformáticas para análisis de enfermedades raras"
        )

    def _initialize_steps(self):
        """
        Inicializa los steps específicos para este workflow.
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
        Configura los métodos mínimos para cada step específico de este workflow.
        """
        # Configuración de filtros para Pharos
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
        
        # Configuración de métodos mínimos por step
        self._minium_methods_by_step = {
            "Pharos_Step": {
                "step_name": "Pharos",
                "processor": "PharosProcessor",
                "methods": [
                    {"METHOD_ID": "df_info", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "df_omim", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "create_protein_protein_relations_df", "METHOD_PARSER_FILTERS": self.filtros_parser_pharos_front[0]},
                    {"METHOD_ID": "df_vias", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "df_numero_vias_por_fuente", "METHOD_PARSER_FILTERS": ""}
                ]
            },
            "Selleckchem_Step": {
                "step_name": "Selleckchem",
                "processor": "SelleckchemProcessor",
                "methods": [
                    {"METHOD_ID": "obtener_link_selleckchem", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "obtener_links_selleckchem", "METHOD_PARSER_FILTERS": ""}
                ]
            },
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
            "Panther_Step": {
                "step_name": "Panther",
                "processor": "PantherProcessor",
                "methods": [
                    {"METHOD_ID": "get_go_terms", "METHOD_PARSER_FILTERS": ""},
                    {"METHOD_ID": "get_pathways", "METHOD_PARSER_FILTERS": ""}
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
            "Stringdb_Step": {
                "step_name": "Stringdb",
                "processor": "StringdbProcessor",
                "methods": [
                    {"METHOD_ID": "get_interactions", "METHOD_PARSER_FILTERS": ""}
                ]
            }
        }

    def _get_search_param_for_step(self, step_name):
        """
        Sobrescribe el método para proporcionar parámetros de búsqueda específicos por step.
        
        Args:
            step_name (str): Nombre del step
            
        Returns:
            str: Parámetro de búsqueda para el step específico
        """
        # Si hay un parámetro de búsqueda general, usarlo para todos
        if self._search_param:
            return self._search_param
            
        # Si no hay parámetro general, usar valores de prueba específicos
        default_params = {
            "Pharos": "FANCA",
            "Selleckchem": "TCL1",
            "Ensembl": "BRCA1",
            "Opentargets": "ENSG00000118271",
            "Panther": "P02766",
            "Uniprot": "O15360",
            "Stringdb": "ENSP00000360522"
        }
        
        return default_params.get(step_name, "")