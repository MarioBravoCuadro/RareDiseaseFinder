from ...core.BaseClient import BaseClient
import re
"""Módulo para interactuar con la API de UniProt y proporcionar métodos para obtener y validar datos de proteínas."""

UNIPROT_BASE_URL = "https://rest.uniprot.org/uniprotkb"

class UniProtClient(BaseClient):
    """Cliente para interactuar con la API de UniProt"""

    def fetch(self, id: str) -> dict:
        """
        Obtiene información de UniProt usando un ID de UniProt o un símbolo de gen.
        
        Args:
            id (str): UniProt ID o símbolo de gen.
            
        Returns:
            dict: Datos obtenidos de la API.
            
        Raises:
            UniProtHTTPError: Si hay un error en la comunicación con la API.
            UniProtParsingError: Si la respuesta no es un JSON válido.
        """
        uniprot_id_pattern = r"^[OPQ][0-9][A-Z0-9]{3}[0-9]$|^[A-NR-Z][0-9]{5}$"

        if re.match(uniprot_id_pattern, id):
            # Es un UniProt ID
            url = f"{UNIPROT_BASE_URL}/{id}"
        else:
            # Es un símbolo de gen
            reviewed_param = "AND+reviewed:true"
            url = f"{UNIPROT_BASE_URL}/search?query=gene:{id}+{reviewed_param}&format=json"

        return self._get_data(url)


    def _ping_logic(self) -> int:
        """Realiza una petición de ping al servidor de Ensembl para comprobar disponibilidad.
        
        Returns:
            int: Código de estado HTTP de la respuesta o 999 si no es posible conectar.
        """
        server = "https://rest.uniprot.org"
        ext = "/uniprotkb/P05067"
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
