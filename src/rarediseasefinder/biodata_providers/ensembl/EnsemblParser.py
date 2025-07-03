"""
EnsemblParser.py

Módulo para parsear datos obtenidos de Ensembl.
"""

from typing import Dict, Any

import pandas as pd

from ...core.BaseParser import BaseParser
from ...core.constants import STRINGDB_URL_TEMPLATE


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
    
    def parse_external_links(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae enlaces externos relevantes de los datos proporcionados por Ensembl.
        
        Args:
            data (Dict[str, Any]): Diccionario con los datos de Ensembl.
            
        Returns:
            pd.DataFrame: DataFrame con enlaces externos estructurados con nombre y URL.
        """
        external_links = []
        external_link = {
            "Nombre": "STRING DB",
            "Enlace": STRINGDB_URL_TEMPLATE.format(data.get("id", "")),
            "Descripción": "Base de datos de interacciones proteína-proteína.",
        }
        external_links.append(external_link)
        print("EnsemblParser.parse_external_links: Enlaces externos extraídos:", external_links)

        return self.parse_to_dataframe(external_links)