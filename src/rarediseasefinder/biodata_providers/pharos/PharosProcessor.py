from typing import Dict

from .PharosClient import PharosClient
from .PharosParser import PharosParser
from ...core.BaseProcessor import BaseProcessor


class PharosProcessor(BaseProcessor):
    """
    Procesa datos de Pharos mediante PharosClient y PharosParser.
    Obtiene datos de un objetivo y los convierte en DataFrames según filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el procesador de Pharos.
        Configura el cliente, el parser y el mapeo de métodos.
        """
        self.client = PharosClient()
        self.parser = PharosParser()
        super().__init__(self.client,self.parser)
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        """
        Obtiene un diccionario que mapea claves de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Mapeo de filtros a métodos.
        """
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
