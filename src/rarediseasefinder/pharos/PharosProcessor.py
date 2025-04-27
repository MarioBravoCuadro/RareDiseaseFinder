from pandas import DataFrame

from .PharosClient import PharosClient
from .PharosParser import PharosParser
import pandas as pd
from typing import Dict, Any, Optional

class PharosProcessor:
    """
    Clase para procesar datos de Pharos utilizando PharosClient y PharosParser.
    Permite obtener datos de un identificador y filtrarlos según prioridades definidas.
    """
    pharosClient = None
    pharosParser = None

    def __init__(self):
        """
        Inicializa el procesador creando instancias de PharosClient y PharosParser.
        """
        self.pharosClient = PharosClient()
        self.pharosParser = PharosParser()

    filters =[
            {
                "procesador":"Pharos",
                "prioridad_clases":{
                    "Tclin": 1,
                    "Tchem": 2,
                    "Tbio": 3,
                    "Tdark": 4
                },
                "prioridad_propiedades":{
                    "p_wrong": 1,
                    "p_ni": 2
                    # "p_int": 3,
                    # "novelty": 4
                }
            },
            {
                "procesador": "Uniprot",
            },
            {
                "procesador": "Selleckchem",
            }
    ]

    def getFilters(self, filters: list) -> Dict[str, Dict]:
        """
        Devuelve los filtros de prioridad para el procesador 'Pharos'.
        Args:
            filters (list): Lista de diccionarios de filtros.
        Returns:
            Dict[str, Dict]: Diccionario con prioridades de clases y propiedades.
                            Si no se encuentra, devuelve un diccionario vacío.
        """
        for processor in filters:
            if processor["procesador"] == "Pharos":
                prioridad_clases = processor["prioridad_clases"]
                prioridad_propiedades = processor["prioridad_propiedades"]
                filtros = {
                    "prioridad_clases": prioridad_clases,
                    "prioridad_propiedades": prioridad_propiedades
                }
                return filtros
        # Si no se encuentra, devolver un diccionario vacío en lugar de None
        return {"prioridad_clases": {}, "prioridad_propiedades": {}}

    def fetch(self, identifier: str) -> dict[str, DataFrame] | DataFrame:
        """
        Obtiene y procesa los datos de Pharos para un identificador dado.
        Args:
            identifier (str): Identificador del target a buscar.
        Returns:
            pd.DataFrame: DataFrame con los datos procesados por PharosParser o DataFrame vacío si no hay datos.
        """
        filters = self.getFilters(self.filters)
        prioridad_clases = filters["prioridad_clases"]
        prioridad_propiedades = filters["prioridad_propiedades"]
        data = self.pharosClient.get_target_data(identifier)
        
        if data:
            return self.pharosParser.parse(data, prioridad_clases, prioridad_propiedades)
        return None

    #TODO implementar consulta al cliente mediante un ping a la url de este
    def getStatus(self) -> str:
        return "OK"


