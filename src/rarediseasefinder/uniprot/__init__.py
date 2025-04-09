from .client import UniProtClient
from .parser import UniProtParser

def get_uniprot_data(identifier, search_by_gene=False):
    """
    Obtiene y procesa datos de UniProt a partir de un identificador
    
    Args:
        identifier (str): ID de UniProt o nombre de gen
        search_by_gene (bool): Si es True, busca por nombre de gen en lugar de ID
        
    Returns:
        dict: Diccionario con DataFrames procesados con la información de UniProt
    """
    if search_by_gene:
        data = UniProtClient.search_by_gene(identifier)
        if data and "results" in data and len(data["results"]) > 0:
            data = data["results"][0]
        else:
            return {}
    else:
        data = UniProtClient.get_by_id(identifier)
        
    return UniProtParser.parse_all(data)

__all__ = ['get_uniprot_data', 'UniProtClient', 'UniProtParser']