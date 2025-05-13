"""
Módulo de cliente para la API de Ensembl.
Proporciona clases y métodos para consultar datos de genes vía REST.
"""

from ...core.BaseClient import BaseClient


class EnsemblClient(BaseClient):
    """
    Cliente para interactuar con la API REST de Ensembl.
    Permite construir URLs de consulta y obtener datos de genes por su nombre.
    """
    #url example ?content-type=application/json;expand=1
    path_url = "https://grch37.rest.ensembl.org/lookup/symbol/homo_sapiens/FANCA?content-type=application/json;expand=1"
    query_url = "?content-type=application/json;expand=1"

    def __init__(self):
        """
        Inicializa el cliente de Ensembl.
        """
        pass

    def _create_url_string(self,gen_term )-> str:
        """
        Construye la URL para consultar un gen en Ensembl.
        Args:
            gen_term (str): Nombre del gen a consultar.
        Returns:
            str: URL completa para la consulta.
        """
        return str(self.path_url + gen_term + self.query_url)

    def fetch(self,id:str)->dict:
        """
        Obtiene los datos de un gen desde Ensembl usando su nombre.
        Args:
            gen_term (str): Nombre del gen a consultar.
        Returns:
            dict: Datos obtenidos de la API de Ensembl.
        """
        url = self._create_url_string(id)
        return self._get_data(url)
    
    def _ping_logic(self) -> int:
        """
        Comprueba la conexión con el servidor de Ensembl.
        Returns:
            int: Código de estado HTTP de la respuesta o 999 si falla la conexión.
        """

        server = "https://grch37.rest.ensembl.org"
        ext = "/info/ping?"
        url = server+ext
        if self._try_connection(url):
            response = EnsemblClient._http_response(url)
            return response.status_code
        else:
            return 999

    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos de Ensembl.
        """
        pass
