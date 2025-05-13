"""
Módulo para procesar datos de OpenTargets combinando cliente y parser.
"""
from typing import Dict

from .OpenTargetsClient import OpenTargetsClient
from .OpenTargetsParser import OpenTargetsParser
from ...core.BaseProcessor import BaseProcessor


class OpenTargetsProcessor(BaseProcessor):
    """
    Procesa datos de OpenTargets mediante OpenTargetsClient y OpenTargetsParser.
    Obtiene datos de genes y los convierte en DataFrames según filtros proporcionados.
    """
    
    def __init__(self):
        """
        Inicializa el procesador de OpenTargets.
        Configura el cliente, el parser y el mapeo de métodos.
        """
        self.client = OpenTargetsClient()
        self.parser = OpenTargetsParser()
        super().__init__(self.client, self.parser)
    
    def get_method_map(self) -> Dict[str, str]:
        """
        Obtiene un diccionario que mapea claves de filtros a nombres de métodos del parser.
        
        Returns:
            Dict[str, str]: Mapeo de filtros a métodos.
        """
        return {
            "basic_info": "create_basic_info_df",
            "pathways": "create_pathways_df",
            "known_drugs": "create_known_drugs_df",
            "associated_diseases": "create_associated_diseases_df",
            "interactions": "create_interactions_df",
            "mouse_phenotypes": "create_mouse_phenotypes_df"
        }