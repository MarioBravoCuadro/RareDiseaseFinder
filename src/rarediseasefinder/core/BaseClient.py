from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

import requests
from ..core.BaseRetriever import BaseRetriever
from .errors import BaseHTTPError, BaseParsingError, BaseError

class BaseClient(BaseRetriever, ABC):
    """Cliente base para interactuar con la API """
    
    @staticmethod
    def _fetch_response(url) -> requests.Response:
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
            return response
        except requests.exceptions.HTTPError as http_err:
            raise BaseHTTPError(f"HTTP error: {http_err}")
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")
    
    @staticmethod
    def _fetch_data(url) -> requests.Response:
        """
        Método privado para devolver la respuesta en json
        
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
            response = BaseClient._fetch_response(url)
            return response
        except ValueError as json_err:
            raise BaseParsingError(f"JSON inválido: {json_err}")
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")
        
    @staticmethod
    def _post_data(url: str, json: Optional[Dict[str, Any]] = None,
                  data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> requests.Response:
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
            return response
        except requests.exceptions.HTTPError as http_err:
            raise BaseHTTPError(f"HTTP error: {http_err}")
        except ValueError as json_err:
            raise BaseParsingError(f"JSON inválido: {json_err}")
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")
    
    def check_connection(self):
        """
        Verifica la disponibilidad de la API o servicio asociado al cliente.
        
        Este método debe ser implementado por las clases derivadas para proporcionar
        una verificación específica de la conexión con su respectivo servicio.
        
        Raises:
            BaseHTTPError: Si hay un error en la comunicación con la API
        """
        response = self._ping_logic()
        if not response.ok:
            error_code = f"Connection error: {response.status_code}"
            raise BaseHTTPError(error_code)
            
    @abstractmethod
    def _ping_logic(self) -> requests.Response:
        """
        Establece la lógica de conexión para las clases derivadas.

        Este método debe ser implementado por las clases derivadas para proporcionar
        una implementación específica de la lógica de conexión con el servicio correspondiente.

        Returns:
            requests.Response: La respuesta de la conexión establecida.
        """
        pass