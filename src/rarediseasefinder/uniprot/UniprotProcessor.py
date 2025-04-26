from .UniProtClient import UniProtClient
from .UniProtParser import UniProtParser


class UniprotProcessor:

    uniprotClient = None
    uniprotParser = None

    def __init__(self):
        self.uniprotClient = UniProtClient()
        self.uniprotParser = UniProtParser()

        pass
    def get_uniprot_data(self,identifier, search_by_gene=False) -> dict:
        """
        Obtiene y procesa datos de UniProt a partir de un identificador

        Args:
            identifier (str): ID de UniProt o nombre de gen
            search_by_gene (bool): Si es True, busca por nombre de gen en lugar de ID

        Returns:
            dict: Diccionario con DataFrames procesados con la información de UniProt
        """
        if search_by_gene:
            data = self.uniprotClient.search_by_gene(identifier)
            if data and "results" in data and len(data["results"]) > 0:
                data = data["results"][0]
            else:
                return {}
        else:
            data = UniProtClient.get_by_id(identifier)

        return UniProtParser.parse_all(data)

    #TODO implementar consulta al cliente mediante un ping a la url de este
    def getStatus(self) -> str:
        return "OK"