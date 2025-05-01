import requests
from abc import ABC, abstractmethod
from ..core.errors import BaseHTTPError

class BaseRetriever(ABC):
    """
    Clase base abstracta para recuperadores de información.

    Esta clase define la interfaz y la lógica básica para verificar la conexión
    con un servicio o API. Las clases derivadas deben implementar la lógica
    específica de conexión.
    """

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

    def check_connection(self):
        """
        Verifica la disponibilidad de la API o servicio asociado al recuperador de información.
        
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
    def check_data(data: | ) -> bool:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            bool: _description_
        """
    pass
