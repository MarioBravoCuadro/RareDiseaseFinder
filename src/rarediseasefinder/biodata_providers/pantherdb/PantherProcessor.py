from typing import Dict

from rarediseasefinder.biodata_providers.pantherdb.PantherClient import PantherClient
from rarediseasefinder.biodata_providers.pantherdb.PantherParser import PantherParser
from src.rarediseasefinder.core.BaseProcessor import BaseProcessor


class PantherProcessor(BaseProcessor):
    """
    Procesador para datos de PantherDB.
    Esta clase gestiona el procesamiento de consultas y respuestas del servicio PantherDB.
    """
    
    def __init__(self):
        """
        Inicializa el procesador con el cliente y el parser correspondiente.
        """
        self.client = PantherClient()
        self.parser = PantherParser()
        super().__init__(self.client, self.parser)

    def get_method_map(self) -> Dict[str, str]:
        """
        Proporciona un mapeo entre operaciones y métodos del parser.
        
        Returns:
            Dict[str, str]: Diccionario que relaciona el nombre de la operación con el método del parser.
        """
        return {
            "panther_class": "get_annotation_name"
        }