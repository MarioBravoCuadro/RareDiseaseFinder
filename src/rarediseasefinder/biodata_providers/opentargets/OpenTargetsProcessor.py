"""
Módulo para procesar datos de OpenTargets combinando cliente y parser.
"""
from typing import Dict, Any

import pandas as pd

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
        self.method_map = self.get_method_map()
    
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
    
    def fetch(self, filters: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Obtiene los datos del gen usando el cliente y los procesa con el parser según los filtros.
        
        Args:
            filters (Dict[str, Any]): Filtros de búsqueda y métodos de parser.
            
        Returns:
            Dict[str, pd.DataFrame]: Diccionario de DataFrames procesados por el parser.
            
        Raises:
            ValueError: Si no se encuentra un ID de Ensembl en los parámetros de búsqueda.
        """
        search_params = self.client_filters(filters)
        if not search_params or 'search_id' not in search_params:
            raise ValueError("No se encontró un ID de Ensembl en los parámetros de búsqueda para OpenTargetsProcessor.")
        
        ensembl_id = search_params['search_id']
        data = self.client.get_target_data(ensembl_id)
        return self.parse_filters(data, filters)