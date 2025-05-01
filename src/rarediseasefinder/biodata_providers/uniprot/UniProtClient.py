from ...core.BaseClient import BaseClient
UNIPROT_BASE_URL = "https://rest.uniprot.org/uniprotkb"

class UniProtClient(BaseClient):
    """Cliente para interactuar con la API de UniProt"""

    def get_by_id(self, uniprot_id) -> dict:
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
        return self._fetch_data(url).json()

    def search_by_gene(self, gene_name, reviewed_only=True)->dict:
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
        return self._fetch_data(url).json()

    def get_target_data(self, target_id):
        """
        Obtiene los datos de una proteína por su ID de UniProt.
        Args:
            target_id (str): Identificador de UniProt.
        Returns:
            dict: Datos crudos de la respuesta de la API.
        """
        return self.get_by_id(target_id)

    def _ping_logic(self):
        pass
    def check_data(self):
        pass
