from src.rarediseasefinder.core.BaseClient import BaseClient


class StringDbClient(BaseClient):
    """
    Cliente para interactuar con la API de la base de datos STRING.
    
    Este cliente proporciona métodos para obtener datos de interacción de proteínas
    desde la base de datos STRING.
    """
    STRINGDB_PING_URL = "https://string-db.org/api/json/version"
    STRINGDB_BASE_URL = "https://string-db.org/api/json/get_string_ids?identifiers="
    def __init__(self):
        """Inicializa el cliente de la base de datos STRING."""
        pass

    def create_url(self, id:str)->str:
        """
        Crea una URL para la petición a la API de STRING.
        
        Args:
            id (str): El identificador de la proteína.
            
        Returns:
            str: La URL formateada para la petición a la API.
        """
        return str(self.STRINGDB_BASE_URL + id)

    def fetch(self,id: str) -> dict:
        """
        Obtiene datos de la base de datos STRING para la proteína especificada.
        
        Args:
            id (str): El identificador de la proteína.
            
        Returns:
            dict: Los datos recuperados de la base de datos STRING.
        """
        return self._get_data(self.create_url(id))

    def _ping_logic(self) -> int:
        """
        Comprueba la conectividad con la base de datos STRING.
        
        Returns:
            int: Código de estado HTTP de la petición ping, o 999 si la conexión falló.
        """
        if self._try_connection(self.STRINGDB_PING_URL):
            response = self._http_response(self.STRINGDB_PING_URL)
            return response.status_code
        else:
            return 999

    def check_data(self, data: str | dict) -> bool:
        """
        Valida los datos recibidos de la base de datos STRING.
        
        Args:
            data (str | dict): Los datos a validar, ya sea como cadena o diccionario.
            
        Returns:
            bool: True si los datos son válidos, False en caso contrario.
        """
        pass
