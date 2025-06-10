from abc import ABC
from typing import Optional, Dict, Any

import requests

from .errors import BaseHTTPError, BaseParsingError, BaseError
from ..core.BaseRetriever import BaseRetriever


class BaseClient(BaseRetriever, ABC):
    """Cliente base para interactuar con la API """

    def _get_data(self, url: str, stream: bool = False) -> Any:
        """
        Método privado para devolver la respuesta en json o el objeto response completo
        
        Args:
            url (str): URL a consultar
            stream (bool): Si se debe transmitir la respuesta (por defecto es False)
            
        Returns:
            dict o Response: Datos JSON de la respuesta o el objeto Response completo si stream=True
            
        Raises:
            BaseHTTPError: Si hay un error en la comunicación con la API
            BaseParsingError: Si la respuesta no es un JSON válido
            BaseError: Para cualquier otro error inesperado
        """
        try:
            response = self._http_response(url, stream=stream)
            
            # Si es streaming, devolver el objeto response directamente
            if stream:
                return response
            
            # Si no es streaming, procesar como JSON normalmente
            return response.json()
        except ValueError as json_err:
            # Solo lanzar este error si no es streaming
            if not stream:
                raise BaseParsingError(f"JSON inválido: {json_err}")
            return {"error": f"Error al decodificar JSON: {json_err}"}
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
            return response
        except requests.exceptions.HTTPError as http_err:
            raise BaseHTTPError(f"HTTP error: {http_err}")
        except ValueError as json_err:
            raise BaseParsingError(f"JSON inválido: {json_err}")
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")