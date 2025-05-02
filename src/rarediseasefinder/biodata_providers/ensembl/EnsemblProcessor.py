"""
EnsemblProcessor.py

Módulo para procesar datos de Ensembl usando EnsemblClient y EnsemblParser.
"""

from typing import Dict

import pandas as pd

from .EnsemblClient import EnsemblClient
from .EnsemblParser import EnsemblParser
from ...core.BaseProcessor import BaseProcessor


class EnsemblProcessor(BaseProcessor):
    """
    Clase para procesar datos de Ensembl utilizando EnsemblClient y EnsemblParser.
    Permite obtener el identificador Ensembl de un gen dado su nombre.
    """
    def __init__(self):
        """
        Inicializa el procesador con cliente y parser de Ensembl.
        """
        self.client = EnsemblClient()
        self.parser = EnsemblParser()
        super().__init__(self.client,self.parser)
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        """
        Retorna un mapeo de métodos de parser a las claves de datos.

        Returns:
            Dict[str, str]: Diccionario mapping 'ensembl_id' a 'parse_id'.
        """
        return {
            "ensembl_id": "parse_id"
        }

    def fetch(self, filters: dict) -> Dict[str, pd.DataFrame]:
        """
        Realiza la obtención y parseo de datos de Ensembl según filtros.

        Args:
            filters (dict): Filtros para la consulta; debe incluir 'search_id'.

        Returns:
            Dict[str, pd.DataFrame]: DataFrames resultantes o diccionario vacío.
        """
        search_params = self.client_filters(filters)
        if not search_params or "search_id" not in search_params:
            print("Error: No se encontró un search_id válido en los filtros")
            return {}
        search_id = search_params["search_id"]
        data = self.client.get_by_gene(search_id)
        if data:
            return self.parse_filters(data, filters)
        return {}