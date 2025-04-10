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
        
    @staticmethod
    def _post_data(url: str, json: Optional[Dict[str, Any]] = None,
                  data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Dict:
        """
        Método para realizar solicitudes HTTP POST
        
        Args:
            url (str): URL a consultar
            json (dict, optional): Datos JSON para enviar en el cuerpo
            data (dict, optional): Datos de formulario para enviar en el cuerpo
            headers (dict, optional): Cabeceras HTTP
            
        Returns:
            dict: Datos JSON de la respuesta
            
        Raises:
            BaseHTTPError: Si hay un error en la comunicación con la API
            BaseParsingError: Si la respuesta no es un JSON válido
            BaseError: Para cualquier otro error inesperado
        """
        try:
            response = requests.post(url, json=json, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise BaseHTTPError(f"HTTP error: {http_err}")
        except ValueError as json_err:
            raise BaseParsingError(f"JSON inválido: {json_err}")
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")