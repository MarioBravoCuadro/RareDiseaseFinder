import json
from abc import ABC
from platform import processor
from typing import Dict, Any
from ..IWorkflowStep import IWorkflowStep
from ...core.BaseFilter import BaseFilter
from ...core.BaseProcessor import BaseProcessor

class BaseWorkflowStep(IWorkflowStep, ABC):
    """
    Clase base abstracta para todos los pasos de workflow.
    Implementa la funcionalidad común compartida por todos los pasos.
    """
    
    def __init__(self, name: str, description: str, processor: BaseProcessor, filters:BaseFilter = None):
        """
        Inicializa el paso de workflow con sus atributos básicos.
        
        Args:
            name (str): Nombre identificativo del paso
            description (str): Descripción de la funcionalidad del paso
            processor (BaseProcessor): Procesador específico para este paso
        """
        self.name = name
        self.description = description
        self.processor = processor
        self.filters = filters
        self.status_code = self.processor.get_status_code()

    def get_status_code(self) -> int:
        """
        Obtiene el código de estado del procesador.
        
        Returns:
            int: Código de estado HTTP o código de error
        """
        return self.status_code

    def process(self) -> dict:
        """
        Ejecuta el procesamiento usando el procesador configurado.
        
        Returns:
            dict: Resultados del procesamiento
        """
        if not self.filters:
            raise ValueError("Los filtros deben establecerse antes de procesar")
        return self.processor.fetch(json.loads(self.filters.get_json_str()))

    def revert(self) -> None:
        """
        Revierte las operaciones realizadas por este paso.
        Por defecto no realiza ninguna acción.
        """
        pass    

    def set_filters(self, filters:BaseFilter):
        """
        Establece los filtros para el procesamiento de datos.

        Args:
            filters: Los filtros a aplicar en la consulta.
        """
        self.filters = filters

    def get_filters(self)->BaseFilter:
        """
        Devuelve filtros.
      """
        return self.filters

    def get_method_map(self):
        """
        Obtiene el mapa de métodos disponibles del procesador.
        
        Returns:
            dict: Diccionario con el mapeo de métodos disponibles en el procesador
        """
        return self.processor.method_map