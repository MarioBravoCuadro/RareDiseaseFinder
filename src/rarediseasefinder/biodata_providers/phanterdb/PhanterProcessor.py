import json
from typing import Dict

from src.rarediseasefinder.biodata_providers.phanterdb.PhanterClient import PhanterClient
from src.rarediseasefinder.biodata_providers.phanterdb.PhanterParser import PhanterParser
from src.rarediseasefinder.core.BaseProcessor import BaseProcessor


class PhanterProcessor(BaseProcessor):
    """
    Procesador para datos de PantherDB.
    Esta clase gestiona el procesamiento de consultas y respuestas del servicio PantherDB.
    """
    
    def __init__(self):
        """
        Inicializa el procesador con el cliente y el parser correspondiente.
        """
        self.client = PhanterClient()
        self.parser = PhanterParser()
        super().__init__(self.client, self.parser)

    def get_method_map(self) -> Dict[str, str]:
        """
        Proporciona un mapeo entre operaciones y métodos del parser.
        
        Returns:
            Dict[str, str]: Diccionario que relaciona el nombre de la operación con el método del parser.
        """
        return {
            "annotation_name": "get_annotation_name"
        }