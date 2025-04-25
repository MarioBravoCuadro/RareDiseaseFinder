import pandas as pd
from ..core.parser import BaseParser


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

    def parse_id(self, data: dict) -> str:
        """
        Extrae el identificador 'id' de los datos proporcionados por Ensembl.
        Args:
            data (dict): Diccionario con los datos de Ensembl.
        Returns:
            str: Identificador extraído del diccionario.
        """
        return data["id"]