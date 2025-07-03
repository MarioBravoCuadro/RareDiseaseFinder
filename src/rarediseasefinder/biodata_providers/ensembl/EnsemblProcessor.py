"""
EnsemblProcessor.py

Módulo para procesar datos de Ensembl usando EnsemblClient y EnsemblParser.
"""

from typing import Dict

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

    def get_method_map(self) -> Dict[str, str]:
        """
        Retorna un mapeo de métodos de parser a las claves de datos.

        Returns:
            Dict[str, str]: Diccionario mapping 'ensembl_id' a 'parse_id'.
        """
        return {
            "ensembl_id": "parse_id",
            "external_links": "parse_external_links",
        }