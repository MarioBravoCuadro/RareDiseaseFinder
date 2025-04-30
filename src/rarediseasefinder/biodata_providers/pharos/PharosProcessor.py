from pandas import DataFrame

from ...core.BaseProcessor import BaseProcessor
from .PharosClient import PharosClient
from .PharosParser import PharosParser
from typing import Dict, Optional
import pandas as pd

class PharosProcessor(BaseProcessor):
    """
    Clase para procesar datos de Pharos utilizando PharosClient y PharosParser.
    Permite obtener datos de un identificador y filtrarlos según prioridades definidas.
    """
    def __init__(self):
        super().__init__()
        self.client = PharosClient()
        self.parser = PharosParser()
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        return {
            "df_info": "create_info_df",
            "df_omim": "create_omim_df",
            "create_protein_protein_relations_df": "create_protein_protein_relations_df",
            "df_numero_vias_por_fuente": "create_numero_vias_por_fuente_df",
            "df_vias": "create_vias_df"
        }

    def fetch(self, filters: dict) -> dict:
        """
        Obtiene los datos del target usando el cliente y los procesa con el parser según los filtros.
        Args:
            filters (dict): Filtros de búsqueda y métodos de parser.
        Returns:
            dict: Diccionario de DataFrames procesados por el parser.
        """
        search_params = self.client_filters(filters)
        if not search_params or 'search_id' not in search_params:
            raise ValueError("No se encontró 'search_id' en los parámetros de búsqueda para PharosProcessor.")
        target_id = search_params['search_id']
        data = self.client.get_target_data(target_id)
        return self.parse_filters(data, filters)


