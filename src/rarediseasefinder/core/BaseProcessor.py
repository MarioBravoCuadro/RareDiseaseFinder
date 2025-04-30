from typing import Dict, Any, Optional
import pandas as pd
from .errors import BaseHTTPError

class BaseProcessor:
    """
    Clase base para todos los procesadores de datos biológicos.
    Proporciona una estructura común y métodos básicos que pueden ser utilizados
    o sobreescritos por las clases derivadas.
    """
    
    def __init__(self):
        """
        Inicializa el procesador base.
        Las clases derivadas deben inicializar sus clientes y parsers específicos.
        """
        self.client = None
        self.parser = None
        self.method_map = self.get_method_map()

    def get_method_map(self) -> Dict[str, str]:
        """
        Devuelve un diccionario que mapea nombres de métodos a sus implementaciones.
        Las clases derivadas pueden sobreescribir este método para proporcionar su propio mapeo.
        
        Returns:
            Dict[str, str]: Mapeo de nombres de métodos.
        """
        return {}

    def get_status(self) -> str:
        """
        Verifica el estado de la conexión con la fuente de datos.
        
        Returns:
            str: "OK" si la fuente de datos está disponible, 
                 otro mensaje si hay problemas.
        """
        if hasattr(self.client, 'check_connection') and callable(self.client.check_connection):
            try:
                return self.client.check_connection()
            except BaseHTTPError as e:
                return f"Connection error: {e}"
        return "OK"

    def fetch(self, filters: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Método abstracto. Debe ser implementado por cada procesador hijo según el método de su cliente.
        """
        raise NotImplementedError("Cada procesador hijo debe implementar fetch según su cliente.")

    def parse_filters(self, data: Dict[str, Any], filters: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Procesa los datos según los filtros configurados.
        
        Args:
            data (Dict[str, Any]): Datos obtenidos del cliente.
            filters (Dict[str, Any]): Diccionario con configuraciones de filtros.
            
        Returns:
            Dict[str, pd.DataFrame]: Resultados procesados por los métodos del parser.
        """
        if not self.parser:
            raise NotImplementedError("El parser no está definido.")
        results = {}
        for processor in filters:
            if processor.get("PROCESSOR") == self.__class__.__name__:
                for method_config in processor.get("METODOS_PARSER", []):
                    method_name = method_config.get("NOMBRE_METODO", "")
                    filter_params = method_config.get("FILTROS_METODO_PARSER", {})
                    parser_method = self.method_map.get(method_name)
                    if parser_method and hasattr(self.parser, parser_method):
                        method = getattr(self.parser, parser_method)
                        try:
                            results[method_name] = method(data, filter_params)
                        except TypeError:
                            results[method_name] = method(data)
                    else:
                        print(f"El procesador {processor['PROCESSOR']} no admite la instrucción {method_name} en el parser.")
        return results

    def client_filters(self, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extrae los parámetros de búsqueda para el cliente desde la configuración de filtros.
        
        Args:
            filters (Dict[str, Any]): Diccionario con configuraciones de procesadores.
            
        Returns:
            Optional[Dict[str, Any]]: Parámetros de búsqueda o None si no se encuentra.
        """
        for processor in filters:
            if processor.get("PROCESSOR") == self.__class__.__name__:
                search_params = processor.get("CLIENT_SEARCH_PARAMS")
                if isinstance(search_params, list) and len(search_params) > 0:
                    return search_params[0]
                return search_params
        return None