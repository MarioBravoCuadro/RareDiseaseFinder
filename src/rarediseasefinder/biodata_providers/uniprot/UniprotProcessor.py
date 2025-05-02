from typing import Dict

from .UniProtClient import UniProtClient
from .UniProtParser import UniProtParser
from ...core.BaseProcessor import BaseProcessor


class UniprotProcessor(BaseProcessor):
    def __init__(self):
        self.client = UniProtClient()
        self.parser = UniProtParser()
        super().__init__(self.client,self.parser)
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        return {
            "function": "parse_function",
            "subcellular_location": "parse_subcellular_location",
            "go_terms": "parse_go_terms",
            "disease": "parse_disease",
            "disease_publications": "parse_disease_publications",
            "interactions": "parse_interactions"
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
            raise ValueError("No se encontró 'search_id' en los parámetros de búsqueda para UniprotProcessor.")
        target_id = search_params['search_id']
        data = self.client.get_target_data(target_id)
        return self.parse_filters(data, filters)