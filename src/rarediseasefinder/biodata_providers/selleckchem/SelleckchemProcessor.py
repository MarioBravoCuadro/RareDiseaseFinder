from pandas import DataFrame

from ..selleckchem import SelleckchemScrapper
from ..selleckchem import SelleckchemParser
import pandas as pd
from typing import Optional, Dict


class SelleckchemProcessor:
    """Clase processor para interactuar con la API de Selleckchem.
    Esta clase permite buscar medicamentos y obtener información relevante.
    """
    scrapper = None
    parser = None

    def __init__(self):
        self.scrapper = SelleckchemScrapper.SelleckchemScrapper()
        self.parser = SelleckchemParser.SelleckchemParser()

    def parseFilters(self, data: dict, filters: dict) -> dict:
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
            if processor["PROCESSOR"] == "SelleckchemProcessor":
                if "METODOS_PARSER" in processor:
                    for method_config in processor["METODOS_PARSER"]:
                        method_name = method_config.get("NOMBRE_METODO", "")
                        filter_params = method_config.get("FILTROS_METODO_PARSER", {})

                        match method_name:
                            case "obtener_link_selleckchem":
                                results[method_name] = self.parser.obtener_link_selleckchem(data)
                            case "obtener_links_selleckchem":
                                results[method_name] = self.parser.obtener_links_selleckchem(data)
                            case _:
                                print(
                                    f"El procesador {processor['PROCESSOR']} no admite la instrucción {method_name} en el parser.")
        return results

    def clientFilters(self, filters: dict) -> Optional[dict]:
        """
        Extrae los parámetros de búsqueda para el cliente Uniprot desde la configuración de filtros.

        Args:
            filters (dict): Lista de diccionarios con configuraciones de procesadores.

        Returns:
            """
        for processor in filters:
            if processor["PROCESSOR"] == "SelleckchemProcessor":
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
        search_params = self.clientFilters(filters)
        if not search_params or "search_id" not in search_params:
            print("Error: No se encontró un search_id válido en los filtros")
            return {}

        search_id = search_params["search_id"]
        data = self.scrapper.buscar_medicamento(search_id)
        if data:
            return self.parseFilters(data, filters)
        return {}
    
    #TODO implementar consulta al cliente mediante un ping a la url de este
    def getStatus(self) -> str:
        return "OK"