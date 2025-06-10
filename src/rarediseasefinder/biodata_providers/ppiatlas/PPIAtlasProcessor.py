from typing import Dict

from ...core.BaseProcessor import BaseProcessor
from .PPIAtlasClient import PPIAtlasClient
from .PPIAtlasParser import PPIAtlasParser


class PPIAtlasProcessor(BaseProcessor):
    """
    Processor para coordinar la obtención y transformación de datos de PPIAtlas.
    """
    
    def __init__(self):
        """
        Inicializa el processor de PPIAtlas con el cliente y parser apropiados.
        """
        client = PPIAtlasClient()
        parser = PPIAtlasParser()
        super().__init__(client, parser)
    
    def get_method_map(self) -> Dict[str, str]:
        """
        Obtiene un diccionario que mapea claves de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Mapeo de filtros a métodos.
        """
        return {
            "ppi_table": "parse_ppi_table"
        }