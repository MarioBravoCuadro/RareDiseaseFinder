from ...core.BaseProcessor import BaseProcessor
from ..selleckchem import SelleckchemScrapper
from ..selleckchem import SelleckchemParser
import pandas as pd
from typing import Optional, Dict

class SelleckchemProcessor(BaseProcessor):
    """Clase processor para interactuar con la API de Selleckchem."""
    def __init__(self):
        self.client = SelleckchemScrapper.SelleckchemScrapper()
        self.parser = SelleckchemParser.SelleckchemParser()
        super().__init__(self.client,self.parser)
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        return {
            "obtener_link_selleckchem": "obtener_link_selleckchem",
            "obtener_links_selleckchem": "obtener_links_selleckchem"
        }

    def fetch(self, filters: dict) -> Dict[str, pd.DataFrame]:
        search_params = self.client_filters(filters)
        if not search_params or "search_id" not in search_params:
            print("Error: No se encontró un search_id válido en los filtros")
            return {}
        search_id = search_params["search_id"]
        data = self.client.buscar_medicamento(search_id)
        if data:
            return self.parse_filters(data, filters)
        return {}
