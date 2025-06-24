"""
EnsemblParser.py

Módulo para parsear datos obtenidos de Ensembl.
"""

from typing import Dict, Any

import pandas as pd

from ...core.BaseParser import BaseParser


class EnsemblParser(BaseParser):
    """
    Clase para parsear datos obtenidos de Ensembl.
    Incluye métodos para extraer identificadores y otra información relevante de los datos de Ensembl.
    """
    def __init__(self):
        """
        Inicializa el parser de Ensembl.
        """
        super().__init__()

    def parse_id(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae el identificador 'id' de los datos proporcionados por Ensembl.
        Args:
            data (Dict[str, Any]): Diccionario con los datos de Ensembl.
        Returns:
            pd.DataFrame: DataFrame con el identificador extraído del diccionario.
        """
        id_data = [data["id"]]
        return self.parse_to_dataframe(id_data)