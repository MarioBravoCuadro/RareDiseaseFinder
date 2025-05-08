from abc import ABC, abstractmethod

import requests

from ..core.errors import BaseError, BaseHTTPError


class BaseRetriever(ABC):
    """
    Clase base abstracta para recuperadores de información.

    Esta clase define la interfaz y la lógica básica para verificar la conexión
    con un servicio o API. Las clases derivadas deben implementar la lógica
    específica de conexión.
    """

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
            #response.raise_for_status() check the status code
            return response
        except requests.exceptions.HTTPError as http_err:
            raise BaseHTTPError(f"HTTP error: {http_err}")
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")
        
    @staticmethod
    def _try_connection(url:str) -> bool:
        try:
            requests.get(url,timeout=15)
            return True
        except requests.exceptions.ConnectionError:
            return False
        except Exception as err:
            raise BaseError(f"Error inesperado: {err}")

    @abstractmethod
    def _ping_logic(self) -> int:
        """
        Establece la lógica de conexión para las clases derivadas.

        Este método debe ser implementado por las clases derivadas para proporcionar
        una implementación específica de la lógica de conexión con el servicio correspondiente.

        Returns:
            requests.Response: La respuesta de la conexión establecida.
        """
        pass

    def get_connection_code(self) -> int:
        """
        Devuelve el código asociado a una conexión. Este código puede ser HTTP o un código de error.
        
        Returns:
            int: Código de estado HTTP de la conexión o código de error.
        """
        response = self._ping_logic()
        return response

    @abstractmethod
    def check_data(self, data: str | dict) -> bool:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            bool: _description_
        """
        raise NotImplementedError("Método check_data no implementado en BaseRetriever.")