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

    @abstractmethod
    def fetch(self,id: str) -> dict:
        """
        Método abstracto para recuperar datos.

        Este método debe ser implementado por las clases derivadas para proporcionar
        la lógica específica de recuperación de datos.

        Args:
            id (str): Identificador del recurso a recuperar.

        Returns:
            dict: Datos recuperados.
        """
        pass

    @staticmethod
    def _http_response(url: str, stream: bool = False) -> requests.Response:
        """
        Método privado para realizar solicitudes HTTP
        
        Args:
            url (str): URL a consultar
            stream (bool): Si se debe transmitir la respuesta (por defecto es False)
            
        Returns:
            requests.Response: Datos JSON de la respuesta
            
        Raises:
            BaseHTTPError: Si hay un error en la comunicación con la API
            BaseParsingError: Si la respuesta no es un JSON válido
            BaseError: Para cualquier otro error inesperado
        """
        try:
            response = requests.get(url, stream=stream, timeout=15)
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
            int: Código de estado HTTP de la respuesta o 999 si falla la conexión.
        """
        pass

    def get_connection_code(self) -> int:
        """
        Devuelve el código asociado a una conexión. Este código puede ser HTTP o un código de error.
        Actúa como wrapper para el método _ping_logic.
        
        Returns:
            int: Código de estado HTTP de la conexión o código de error.
                Los códigos de error son:
                - 1001: Error del scrapper al iniciar el driver
                - 999: Error de conexión
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
        pass