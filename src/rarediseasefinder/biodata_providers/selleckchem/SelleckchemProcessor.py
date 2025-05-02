from typing import Dict

import pandas as pd

from ..selleckchem import SelleckchemParser
from ..selleckchem import SelleckchemScrapper
from ...core.BaseProcessor import BaseProcessor


class SelleckchemProcessor(BaseProcessor):
    """
    Procesa datos de Selleckchem usando SelleckchemScrapper y SelleckchemParser.
    Obtiene enlaces de productos de un medicamento según filtros.
    """
    def __init__(self):
        """
        Inicializa el procesador de Selleckchem.
        Configura el scrapper, el parser y el mapeo de métodos.
        """
        self.client = SelleckchemScrapper.SelleckchemScrapper()
        self.parser = SelleckchemParser.SelleckchemParser()
        super().__init__(self.client,self.parser)
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        """
        Retorna un mapeo de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Claves de filtros y métodos asociados.
        """
        return {
            "obtener_link_selleckchem": "obtener_link_selleckchem",
            "obtener_links_selleckchem": "obtener_links_selleckchem"
        }

    def fetch(self, filters: dict) -> Dict[str, pd.DataFrame]:
        """
        Ejecuta la búsqueda y parseo de enlaces de productos.

        Args:
            filters (dict): Filtros que deben incluir 'search_id'.
        Returns:
            Dict[str, pd.DataFrame]: DataFrames resultantes del parseo.
        """
        search_params = self.client_filters(filters)
        if not search_params or "search_id" not in search_params:
            print("Error: No se encontró un search_id válido en los filtros")
            return {}
        search_id = search_params["search_id"]
        data = self.client.buscar_medicamento(search_id)
        if data:
            return self.parse_filters(data, filters)
        return {}
