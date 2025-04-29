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
                    return "NOT OK"
        return "OK"
    
    def fetch(self, params: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Método genérico para obtener datos de una fuente.
        
        Args:
            params (Dict[str, Any]): Parámetros para la consulta.
            
        Returns:
            Dict[str, pd.DataFrame]: Datos obtenidos organizados en DataFrames.
        """
        raise NotImplementedError("El método fetch debe ser implementado por las clases derivadas")
    
    def parse_filters(self, data: Dict[str, Any], filters: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Procesa los datos según los filtros configurados.
        
        Args:
            data (Dict[str, Any]): Datos obtenidos del cliente.
            filters (Dict[str, Any]): Diccionario con configuraciones de filtros.
            
        Returns:
            Dict[str, pd.DataFrame]: Resultados procesados por los métodos del parser.
        """
        raise NotImplementedError("El método parse_filters debe ser implementado por las clases derivadas")
    
    def client_filters(self, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extrae los parámetros de búsqueda para el cliente desde la configuración de filtros.
        
        Args:
            filters (Dict[str, Any]): Diccionario con configuraciones de procesadores.
            
        Returns:
            Optional[Dict[str, Any]]: Parámetros de búsqueda o None si no se encuentra.
        """
        raise NotImplementedError("El método client_filters debe ser implementado por las clases derivadas")