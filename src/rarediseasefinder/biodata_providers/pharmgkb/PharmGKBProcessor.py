from typing import Dict

from ...core.BaseProcessor import BaseProcessor
from .PharmGKBClient import PharmGKBClient
from .PharmGKBParser import PharmGKBParser


class PharmGKBProcessor(BaseProcessor):
    """
    Processor para coordinar la obtención y transformación de datos de PharmGKB.
    """
    
    def __init__(self):
        """
        Inicializa el processor de PharmGKB con el client y el parser apropiados.
        """
        client = PharmGKBClient()
        parser = PharmGKBParser()
        super().__init__(client, parser)
    
    def get_method_map(self) -> Dict[str, str]:
        """
        Obtiene un diccionario que mapea claves de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Mapeo de filtros a métodos.
        """
        return {
            "gene_symbols": "parse_gene_symbols",
            "label_annotations": "parse_label_annotations",
            "literature": "parse_literature",
            "pathways": "parse_pathways"
        }