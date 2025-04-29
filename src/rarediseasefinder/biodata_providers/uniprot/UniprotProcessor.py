from pandas import DataFrame

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

    def parse_filters(self, data: dict, filters: dict) -> dict:
        """
        Procesa los datos según los filtros configurados.

        Args:
            data (dict): Datos obtenidos del cliente Uniprot.
            filters (dict): Diccionario de configuraciones de filtros.

        Returns:
            dict: Resultados procesados por cada método del parser.
        """
        results = {}
        for processor in filters:
            if processor["PROCESSOR"] == "UniprotProcessor":
                if "METODOS_PARSER" in processor:
                    for method_config in processor["METODOS_PARSER"]:
                        method_name = method_config.get("NOMBRE_METODO", "")
                        filter_params = method_config.get("FILTROS_METODO_PARSER", {})

                        match method_name:
                            case "function":
                                results[method_name] = self.uniprotParser.parse_function(data)
                            case "subcellular_location":
                                results[method_name] = self.uniprotParser.parse_subcellular_location(data)
                            case "go_terms":
                                results[method_name] = self.uniprotParser.parse_go_terms(data)
                            case "disease":
                                results[method_name] = self.uniprotParser.parse_disease(data)
                            case "disease_publications":
                                results[method_name] = self.uniprotParser.parse_disease_publications(data)
                            case "interactions":
                                results[method_name] = self.uniprotParser.parse_interactions(data)
                            case _:
                                print(
                                    f"El procesador {processor['PROCESSOR']} no admite la instrucción {method_name} en el parser.")
        return results

    def client_filters(self, filters: dict) -> Optional[dict]:
        """
        Extrae los parámetros de búsqueda para el cliente Uniprot desde la configuración de filtros.

        Args:
            filters (dict): Lista de diccionarios con configuraciones de procesadores.

        Returns:
            Optional[dict]: Parámetros de búsqueda para el cliente Uniprot o None si no se encuentra.
        """
        for processor in filters:
            if processor["PROCESSOR"] == "UniprotProcessor":
                if "CLIENT_SEARCH_PARAMS" in processor:
                    search_params = processor["CLIENT_SEARCH_PARAMS"]
                    # Si SEARCH_PARAMS es una lista, tomar el primer elemento
                    if isinstance(search_params, list) and len(search_params) > 0:
                        return search_params[0]
                    return search_params

        return None  # Si no encuentra el procesador o no tiene SEARCH_PARAMS, devuelve None

    def fetch(self, filters: dict) -> Dict[str, DataFrame]:
        """
        Obtiene y procesa los datos de Uniprot para un identificador dado.

        Args:
            filters (list): Lista de filtros con configuraciones de búsqueda.

        Returns:
            Dict[str, DataFrame]: Diccionario donde las claves son nombres de métodos y
                               los valores son DataFrames con los datos procesados.
        """
        search_params = self.client_filters(filters)
        if not search_params or "search_id" not in search_params:
            print("Error: No se encontró un search_id válido en los filtros")
            return {}

        search_id = search_params["search_id"]
        data = self.uniprotClient.get_by_id(search_id)
        if data:
            return self.parse_filters(data, filters)
        return {}


    #TODO implementar consulta al cliente mediante un ping a la url de este
    def getStatus(self) -> str:
        return "OK"