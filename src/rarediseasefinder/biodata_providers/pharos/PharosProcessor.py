from pandas import DataFrame

from ...core.BaseProcessor import BaseProcessor
from .PharosClient import PharosClient
from .PharosParser import PharosParser
from typing import Dict, Optional

class PharosProcessor(BaseProcessor):
    """
    Clase para procesar datos de Pharos utilizando PharosClient y PharosParser.
    Permite obtener datos de un identificador y filtrarlos según prioridades definidas.
    """

    def __init__(self):
        """
        Inicializa el procesador creando instancias de PharosClient y PharosParser.
        """
        super().__init__()
        self.client = PharosClient()
        self.parser = PharosParser()

    def parse_filters(self, data: dict, filters: dict) -> dict:
        """
        Procesa los datos según los filtros configurados.
        
        Args:
            data (dict): Datos obtenidos del cliente Pharos.
            filters (dict): Diccionario de configuraciones de filtros.
            
        Returns:
            dict: Resultados procesados por cada método del parser.
        """
        results = {}
        for processor in filters:
            if processor["PROCESSOR"] == "PharosProcessor":
                if "METODOS_PARSER" in processor:
                    for method_config in processor["METODOS_PARSER"]:
                        method_name = method_config.get("NOMBRE_METODO", "")
                        filter_params = method_config.get("FILTROS_METODO_PARSER", {})
                        
                        match method_name:
                            case "df_info": 
                                results[method_name] = self.pharosParser.create_info_df(data)
                            case "df_omim": 
                                results[method_name] = self.pharosParser.create_omim_df(data)
                            case "create_protein_protein_relations_df":
                                results[method_name] = self.pharosParser.create_protein_protein_relations_df(data, filter_params)
                            case "df_numero_vias_por_fuente": 
                                results[method_name] = self.pharosParser.create_numero_vias_por_fuente_df(data)
                            case "df_vias": 
                                results[method_name] = self.pharosParser.create_vias_df(data)
                            case _: 
                                print(f"El procesador {processor['PROCESSOR']} no admite la instrucción {method_name} en el parser.")
        return results

    def client_filters(self, filters: dict) -> Optional[dict]:
        """
        Extrae los parámetros de búsqueda para el cliente Pharos desde la configuración de filtros.
        
        Args:
            filters (dict): Lista de diccionarios con configuraciones de procesadores.
            
        Returns:
            Optional[dict]: Parámetros de búsqueda para el cliente Pharos o None si no se encuentra.
        """
        for processor in filters:
            if processor["PROCESSOR"] == "PharosProcessor":
                if "CLIENT_SEARCH_PARAMS" in processor:
                    search_params = processor["CLIENT_SEARCH_PARAMS"]
                    # Si SEARCH_PARAMS es una lista, tomar el primer elemento
                    if isinstance(search_params, list) and len(search_params) > 0:
                        return search_params[0]
                    return search_params
    
        return None  # Si no encuentra el procesador o no tiene SEARCH_PARAMS, devuelve None

    def fetch(self, filters: dict) -> Dict[str, DataFrame]:
        """
        Obtiene y procesa los datos de Pharos para un identificador dado.
        
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
        data = self.pharosClient.get_target_data(search_id)
        if data:
            return self.parseFilters(data, filters)
        return {}


