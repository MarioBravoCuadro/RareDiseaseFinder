from ...core.BaseClient import BaseClient
"""Módulo para interactuar con la API de UniProt y proporcionar métodos para obtener y validar datos de proteínas."""

UNIPROT_BASE_URL = "https://rest.uniprot.org/uniprotkb"

class UniProtClient(BaseClient):
    """Cliente para interactuar con la API de UniProt"""

    def fetch(self, uniprot_id: str) -> dict:
        """
        Obtiene información de una proteína por su ID de UniProt
        
        Args:
            uniprot_id (str): Identificador de UniProt
            
        Returns:
            dict: Datos crudos de la respuesta de la API
            
        Raises:
            UniProtHTTPError: Si hay un error en la comunicación con la API
            UniProtParsingError: Si la respuesta no es un JSON válido
        """
        url = f"{UNIPROT_BASE_URL}/{uniprot_id}"
        return self._get_data(url)

    def fetch(self, gene_name: str, reviewed_only: bool = True) -> dict:
        """
        Busca proteínas por nombre de gen
        
        Args:
            gene_name (str): Nombre del gen a buscar
            reviewed_only (bool): Si es True, solo devuelve entradas revisadas
            
        Returns:
            dict: Resultado de la búsqueda
            
        Raises:
            UniProtHTTPError: Si hay un error en la comunicación con la API
            UniProtParsingError: Si la respuesta no es un JSON válido
        """
        reviewed_param = "AND+reviewed:true" if reviewed_only else ""
        url = f"{UNIPROT_BASE_URL}/search?query=gene:{gene_name}+{reviewed_param}&format=json"
        return self._get_data(url)

    def _ping_logic(self) -> int:
        """Realiza una petición de ping al servidor de Ensembl para comprobar disponibilidad.
        
        Returns:
            int: Código de estado HTTP de la respuesta o 999 si no es posible conectar.
        """
        server = "https://grch37.rest.ensembl.org"
        ext = "/info/ping?"
        url = server+ext
        if self._try_connection(url):
            response = UniProtClient._http_response(url)
            return response.status_code
        else:
            return 999

    def check_data(self):
        """Valida o comprueba los datos obtenidos de UniProt.
        
        Este método puede ser sobrescrito para implementar validaciones específicas.
        """
        pass
