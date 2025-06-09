from ...core.BaseClient import BaseClient

#https://pantherdb.org/services/openAPISpec.jsp
class PantherClient(BaseClient):
    """
    Cliente para la API de PantherDB que permite obtener información genética.
    Implementa los métodos necesarios para comunicarse con el servicio web de PantherDB.
    """

    PHANTER_DOMAIN_URL = f"https://pantherdb.org"
    PHANTER_SERVICE_URL = "/services/oai/pantherdb/geneinfo?geneInputList="
    PHANTER_URL_SUFIX = "&organism=9606"

    def __init__(self):
        """
        Inicializa una instancia del cliente de PantherDB.
        """
        pass

    def _create_url_string(self, gen_term:str) -> str:
        """
        Crea la URL de consulta para PantherDB.
        
        Args:
            gen_term: Término genético para la consulta.
            
        Returns:
            str: URL completa para la consulta a PantherDB.
        """
        return str(self.PHANTER_DOMAIN_URL + self.PHANTER_SERVICE_URL + gen_term + self.PHANTER_URL_SUFIX)

    def fetch(self, id : str) -> dict:
        """
        Obtiene datos de PantherDB para un término genético específico. Puede ser un symbol o un UniprotID.
        
        Args:
            id: Término genético para la consulta.
            
        Returns:
            dict: Datos obtenidos de PantherDB.
        """
        url = self._create_url_string(id)
        return self._get_data(url)

    def _ping_logic(self) -> int:
        """
        Verifica si el servicio de PantherDB está funcionando.
        
        Returns:
            int: Código de estado de la respuesta HTTP o 999 si no hay conexión.
        """
        #TODO Implement a better way to check if the service is up,
        url = self.PHANTER_DOMAIN_URL + self.PHANTER_SERVICE_URL
        if self._try_connection(url):
            response = self._http_response(url)
            return response.status_code
        else:
            return 999

    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos de Phanter.
        """
        pass