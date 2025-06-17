from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union

import pandas as pd

from .BaseRetriever import BaseRetriever
from .BaseParser import BaseParser



class BaseProcessor(ABC):
    """
    Clase base para todos los procesadores de datos biológicos.
    Proporciona una estructura común y métodos básicos que pueden ser utilizados
    o sobreescritos por las clases derivadas.
    """
    
    def __init__(self, retriever : BaseRetriever, parser: BaseParser):
        """
        Inicializa el procesador base.
        Las clases derivadas deben inicializar sus clientes y parsers específicos.
        """
        self.retriever = retriever
        self.parser = parser
        self.method_map = self.get_method_map()

    @abstractmethod
    def get_method_map(self) -> Dict[str, str]:
        """
        Devuelve un diccionario que mapea nombres de métodos a sus implementaciones.
        Las clases derivadas deben implementar este método para proporcionar su propio mapeo.
        
        Returns:
            Dict[str, str]: Mapeo de nombres de métodos.
        """
        pass

    def get_status_code(self) -> int:
        status = self.retriever.get_connection_code()
        return status

    def fetch(self, filters: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Obtiene los datos del gen usando el cliente y los procesa con el parser según los filtros.
        
        Args:
            filters (Dict[str, Any]): Filtros de búsqueda y métodos de parser.
            
        Returns:
            Dict[str, pd.DataFrame]: Diccionario de DataFrames procesados por el parser.
            
        Raises:
            ValueError: Si no se encuentra un ID de la fuente en los parámetros de búsqueda.
        """
        search_params = self.retriever_filters(filters)
        if not search_params or 'search_id' not in search_params:
            raise ValueError("No se encontró un identificador de la fuente en los parámetros de búsqueda para el procesador.")
        
        search_id = search_params['search_id']
        data = self.retriever.fetch(search_id)
        return self.parse_filters(data, filters)

    def parse_filters(self, data: Dict[str, Any], filters: list[str, Any]) -> Dict[str, pd.DataFrame]:
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
        print(type(filters))
        print(type(data))

        for processor in filters:
            if processor.get("PROCESSOR") == self.__class__.__name__:
                for method_config in processor.get("METODOS_PARSER", []):
                    method_name = method_config.get("NOMBRE_METODO", "")
                    filter_params = method_config.get("FILTROS_METODO_PARSER", {})
                    parser_method = self.method_map.get(method_name)
                    if parser_method and hasattr(self.parser, parser_method):
                        method = getattr(self.parser, parser_method)
                        try:
                            # Obtener el resultado del método del parser
                            result = method(data, filter_params)
                            
                            # Verificar si hay instrucción de agrupación en los filtros
                            group_by_column = filter_params.get("group_by")
                            
                            # Si el resultado es un DataFrame y se especificó group_by
                            if isinstance(result, pd.DataFrame) and group_by_column and group_by_column in result.columns and not result.empty:
                                # Realizar la agrupación
                                grouped_dfs = []
                                for group_value, group_df in result.groupby(group_by_column):
                                    # Resetear índices
                                    group_df = group_df.reset_index(drop=True)
                                    # Guardar valor de grupo como metadato
                                    group_df.attrs['group_value'] = group_value
                                    grouped_dfs.append(group_df)
                                
                                # Si solo hay un grupo, mantenerlo como DataFrame único para compatibilidad
                                if len(grouped_dfs) == 1:
                                    results[method_name] = grouped_dfs[0]
                                else:
                                    results[method_name] = grouped_dfs
                            else:
                                # Mantener el resultado original (ya sea DataFrame o lista)
                                results[method_name] = result
                                
                        except TypeError:
                            # Sin filtros, llamar al método sin parámetros
                            result = method(data)
                            
                            # Si se especificó group_by, intentar agrupar también
                            group_by_column = filter_params.get("group_by")
                            if isinstance(result, pd.DataFrame) and group_by_column and group_by_column in result.columns and not result.empty:
                                # Lógica de agrupación (igual que arriba)
                                grouped_dfs = []
                                for group_value, group_df in result.groupby(group_by_column):
                                    group_df = group_df.reset_index(drop=True)
                                    group_df.attrs['group_value'] = group_value
                                    grouped_dfs.append(group_df)
                                
                                if len(grouped_dfs) == 1:
                                    results[method_name] = grouped_dfs[0]
                                else:
                                    results[method_name] = grouped_dfs
                            else:
                                results[method_name] = result
                    else:
                        print(f"El procesador {processor['PROCESSOR']} no admite la instrucción {method_name} en el parser.")
        return results

    def retriever_filters(self, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
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
    
    def results_to_json(self, results: Dict[str, Union[pd.DataFrame, List[pd.DataFrame]]]) -> Dict[str, Any]:
        """
        Convierte los resultados del procesador en una estructura JSON adecuada para API.
        
        Args:
            results: Resultados del proceso de parseo (DataFrames individuales o listas)
            
        Returns:
            Dict[str, Any]: Estructura JSON para enviar a la API
        """
        json_results = {}
        
        for method_name, result in results.items():
            if isinstance(result, pd.DataFrame):
                # DataFrame individual: convertir directamente
                json_results[method_name] = result.to_dict(orient='records')
            elif isinstance(result, list) and all(isinstance(df, pd.DataFrame) for df in result):
                # Lista de DataFrames: crear estructura agrupada
                if len(result) == 1:
                    # Si solo hay un DataFrame, no usar estructura de grupos
                    json_results[method_name] = result[0].to_dict(orient='records')
                else:
                    grouped_data = {}
                    for i, df in enumerate(result):
                        # Usar el valor de grupo almacenado o un índice numérico
                        group_key = str(df.attrs.get('group_value', f'grupo_{i+1}'))
                        grouped_data[group_key] = df.to_dict(orient='records')
                    json_results[method_name] = grouped_data
            else:
                # Otros tipos de datos (poco probable)
                json_results[method_name] = result
                
        return json_results