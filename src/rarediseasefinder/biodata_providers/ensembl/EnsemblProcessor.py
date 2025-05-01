from ...core.BaseProcessor import BaseProcessor
from .EnsemblClient import EnsemblClient
from .EnsemblParser import EnsemblParser
import pandas as pd
from typing import Optional, Dict

class EnsemblProcessor(BaseProcessor):
    """
    Clase para procesar datos de Ensembl utilizando EnsemblClient y EnsemblParser.
    Permite obtener el identificador Ensembl de un gen dado su nombre.
    """
    def __init__(self):
        self.client = EnsemblClient()
        self.parser = EnsemblParser()
        super().__init__(self.client,self.parser)
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        return {
            "ensembl_id": "parse_id"
        }

    def fetch(self, filters: dict) -> Dict[str, pd.DataFrame]:
        search_params = self.client_filters(filters)
        if not search_params or "search_id" not in search_params:
            print("Error: No se encontró un search_id válido en los filtros")
            return {}
        search_id = search_params["search_id"]
        data = self.client.get_by_gene(search_id)
        if data:
            return self.parse_filters(data, filters)
        return {}