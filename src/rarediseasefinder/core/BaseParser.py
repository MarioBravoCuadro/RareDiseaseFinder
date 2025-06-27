import json
from typing import Union
import re
import pandas as pd

from .errors import BaseError, BaseParsingError
from .constants import NOT_FOUND_MESSAGE, NO_DATA_MARKER

class BaseParser:
    def __init__(self):
        pass
    
    def parse_to_dataframe(self, data: Union[dict, list]) -> pd.DataFrame:
        """
        Transforma datos crudos en un DataFrame de pandas.
        
        Args:
            data: Datos a parsear (dict, list o estructura anidada de list o dict).
                        
        Returns:
            pd.DataFrame: Datos estructurados en tabla.
            
        Raises:
            ParseError: Si los datos no pueden convertirse a DataFrame.
        """
        
        if not data or (isinstance(data, dict) and not data) or (isinstance(data, list) and not data):
            return pd.DataFrame([{NO_DATA_MARKER: NOT_FOUND_MESSAGE}])
    
        try:
            if isinstance(data, list):
                return pd.DataFrame(data).fillna(NOT_FOUND_MESSAGE)
            elif isinstance(data, dict):
                if all(isinstance(v, (dict, list)) for v in data.values()):
                    return pd.json_normalize(data, sep="_").fillna(NOT_FOUND_MESSAGE)
                return pd.DataFrame([data]).fillna(NOT_FOUND_MESSAGE)
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

        return pd.json_normalize(json_data).fillna(NOT_FOUND_MESSAGE)

    def clean_html(html_text: str) -> str:
        """
        Limpia texto HTML básico para presentación en DataFrame.
        """
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html_text)
