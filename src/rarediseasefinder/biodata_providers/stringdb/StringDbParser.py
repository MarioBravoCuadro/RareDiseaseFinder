import pandas as pd
from ...core.BaseParser import BaseParser

class StringDbParser(BaseParser):
    """
    Analizador para datos de la base de datos STRING.
    
    Esta clase procesa y transforma los datos recuperados de la base de datos STRING
    en formatos estandarizados para un análisis posterior.
    """
    def __init__(self):
        """Inicializa el analizador de la base de datos STRING."""
        super().__init__()

    def get_annotation(self, data: dict) -> pd.DataFrame:
        """
        Extrae y analiza datos de anotación de la respuesta de la base de datos STRING.
        
        Args:
            data (dict): Datos sin procesar devueltos por la API de STRING.
            
        Returns:
            pd.DataFrame: Un DataFrame que contiene el nombre preferido y la información
                        de anotación para la proteína consultada.
        """
        name = data[0].get("preferredName", "")
        description = data[0].get("annotation", "")
        result = {"Prefered name" : name, "Annotation" : description}
        return self.parse_to_dataframe(result)