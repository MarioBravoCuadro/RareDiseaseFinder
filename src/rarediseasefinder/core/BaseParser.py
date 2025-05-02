import json
from typing import Union

import pandas as pd

from .errors import BaseError, BaseParsingError


class BaseParser:
    def __init__(self):
        pass
    
    def parse_to_dataframe(self, data: Union[dict, list], **kwargs) -> pd.DataFrame:
        """
        Transforma datos crudos en un DataFrame de pandas.
        
        Args:
            data: Datos a parsear (dict, list o estructura anidada).
            kwargs: Parámetros adicionales para personalizar el parsing.
            
        Returns:
            pd.DataFrame: Datos estructurados en tabla.
            
        Raises:
            ParseError: Si los datos no pueden convertirse a DataFrame.
        """
        try:
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                if all(isinstance(v, (dict, list)) for v in data.values()):
                    return pd.json_normalize(data, sep="_")
                return pd.DataFrame([data])
            else:
                raise BaseParsingError(f"Tipo de dato no soportado: {type(data)}")
                
        except Exception as e:
            raise BaseError(f"Error al parsear DataFrame: {str(e)}") from e

    def json_to_dataframe(json_data):
        """
        Convierte un JSON en un DataFrame de pandas.
        :param json_data: Puede ser un diccionario de Python o una cadena JSON.
        :return: DataFrame de pandas.
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)  # Convertir de cadena JSON a diccionario

        return pd.json_normalize(json_data)
