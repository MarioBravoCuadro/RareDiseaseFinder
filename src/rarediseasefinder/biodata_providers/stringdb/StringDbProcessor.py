from typing import Dict
import json

from src.rarediseasefinder.biodata_providers.stringdb.StringDbClient import StringDbClient
from src.rarediseasefinder.biodata_providers.stringdb.StringDbParser import StringDbParser
from src.rarediseasefinder.core.BaseProcessor import BaseProcessor


class StringDbProcessor(BaseProcessor):
    """
    Procesador para operaciones con la base de datos STRING.
    
    Esta clase coordina las interacciones entre StringDbClient y StringDbParser,
    proporcionando una interfaz unificada para obtener y procesar datos de proteínas
    de la base de datos STRING.
    """

    def __init__(self):
        """
        Inicializa el procesador de la base de datos STRING.
        
        Crea instancias de StringDbClient y StringDbParser, e inicializa
        el BaseProcessor padre con estos componentes.
        """
        self.client = StringDbClient()
        self.parser = StringDbParser()
        super().__init__(self.client, self.parser)

    def get_method_map(self) -> Dict[str, str]:
        """
        Proporciona un mapeo entre nombres de métodos y sus implementaciones.
        
        Returns:
            Dict[str, str]: Un diccionario que mapea nombres de métodos a los nombres
                           de sus implementaciones reales.
        """
        return {
            "get_annotation" : "get_annotation"
        }