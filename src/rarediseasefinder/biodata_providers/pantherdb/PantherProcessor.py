from typing import Dict

from .PantherClient import PantherClient
from .PantherParser import PantherParser
from ...core.BaseProcessor import BaseProcessor


class PantherProcessor(BaseProcessor):
    """
    Procesador para datos de PantherDB.
    Esta clase gestiona el procesamiento de consultas y respuestas del servicio PantherDB.
    """
    
    def __init__(self):
        """
        Inicializa el procesador con el cliente y el parser correspondiente.
        """
        client = PantherClient()
        parser = PantherParser()
        super().__init__(client, parser)

    def get_method_map(self) -> Dict[str, str]:
        """
        Proporciona un mapeo entre operaciones y métodos del parser.
        
        Returns:
            Dict[str, str]: Diccionario que relaciona el nombre de la operación con el método del parser.
        """
        return {
            "annotation_name": "get_annotation_name",
            "annotations": "parse_annotations",
            "pathways": "parse_pathways"
        }