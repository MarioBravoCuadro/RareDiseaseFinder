from typing import Dict

import pandas as pd

from ...core.BaseProcessor import BaseProcessor
from .PharmacologyClient import PharmacologyClient
from .PharmacologyParser import PharmacologyParser


class PharmacologyProcessor(BaseProcessor):
    """
    Processor para coordinar la obtención y transformación de datos de Guide to Pharmacology.
    """
    
    def __init__(self):
        """
        Inicializa el processor de Guide to Pharmacology con el client y el parser apropiados.
        """
        client = PharmacologyClient()
        parser = PharmacologyParser()
        super().__init__(client, parser)
    
    def get_method_map(self) -> Dict[str, str]:
        """
        Obtiene un diccionario que mapea claves de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Mapeo de filtros a métodos.
        """
        return {
            "target_id": "parse_target_id",
            "comments": "parse_comments",
            "references": "parse_references",
            "interactions": "parse_interactions"
        }