from .UniProtClient import UniProtClient
from .UniProtParser import UniProtParser
from typing import Dict, Any, Optional, Union
import pandas as pd


class UniprotProcessor:

    uniprotClient = None
    uniprotParser = None

    def __init__(self):
        self.uniprotClient = UniProtClient()
        self.uniprotParser = UniProtParser()

    def get_uniprot_data(self, identifier: str, search_by_gene: bool = False) -> Dict[str, pd.DataFrame]:
        """
        Obtiene y procesa datos de UniProt a partir de un identificador

        Args:
            identifier (str): ID de UniProt o nombre de gen
            search_by_gene (bool): Si es True, busca por nombre de gen en lugar de ID

        Returns:
            Dict[str, pd.DataFrame]: Diccionario con DataFrames procesados con la información de UniProt
        """
        if search_by_gene:
            data = self.uniprotClient.search_by_gene(identifier)
            if data and "results" in data and len(data["results"]) > 0:
                data = data["results"][0]
            else:
                return {}
        else:
            data = UniProtClient.get_by_id(identifier)

        return self.uniprotParser.parse_all(data)

    #TODO implementar consulta al cliente mediante un ping a la url de este
    def getStatus(self) -> str:
        return "OK"