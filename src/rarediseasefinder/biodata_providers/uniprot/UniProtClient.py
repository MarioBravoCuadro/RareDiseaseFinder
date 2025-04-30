from ...core.BaseClient import BaseClient
UNIPROT_BASE_URL = "https://rest.uniprot.org/uniprotkb"

class UniProtClient(BaseClient):
    """Cliente para interactuar con la API de UniProt"""
    
    @classmethod
    def get_by_id(cls, uniprot_id):
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
        return cls._fetch_data(url)
    
    @classmethod
    def search_by_gene(cls, gene_name, reviewed_only=True):
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
        return cls._fetch_data(url)

    def get_target_data(self, target_id):
        """
        Obtiene los datos de una proteína por su ID de UniProt.
        Args:
            target_id (str): Identificador de UniProt.
        Returns:
            dict: Datos crudos de la respuesta de la API.
        """
        return self.get_by_id(target_id)
