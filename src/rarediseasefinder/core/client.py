import requests
from .errors import BaseHTTPError, BaseParsingError, BaseError

class BaseClient:
    """Cliente base para interactuar con la API """
    
    @staticmethod
    def _fetch_data(url):
        """
        Método privado para realizar solicitudes HTTP
        
        Args:
            url (str): URL a consultar
            
        Returns:
            dict: Datos JSON de la respuesta
            
        Raises:
            BaseHTTPError: Si hay un error en la comunicación con la API
            BaseParsingError: Si la respuesta no es un JSON válido
            BaseError: Para cualquier otro error inesperado
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise BaseHTTPError(f"HTTP error: {http_err}")
        except ValueError as json_err:
            raise BaseParsingError(f"JSON inválido: {json_err}")
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")