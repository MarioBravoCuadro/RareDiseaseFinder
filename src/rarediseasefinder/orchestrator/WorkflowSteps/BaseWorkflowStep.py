from abc import ABC
from typing import Dict, Any
from ..IWorkflowStep import IWorkflowStep
from ...core.BaseProcessor import BaseProcessor

class BaseWorkflowStep(IWorkflowStep, ABC):
    """
    Clase base abstracta para todos los pasos de workflow.
    Implementa la funcionalidad común compartida por todos los pasos.
    """
    
    def __init__(self, name: str, description: str, processor: BaseProcessor, filters: Dict[str, Any] = None):
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

    def get_status_code(self) -> int:
        """
        Obtiene el código de estado del procesador.
        
        Returns:
            int: Código de estado HTTP o código de error
        """
        return self.processor.get_status_code()

    def process(self) -> dict:
        """
        Ejecuta el procesamiento usando el procesador configurado.
        
        Returns:
            dict: Resultados del procesamiento
        """
        if not self.filters:
            raise ValueError("Los filtros deben establecerse antes de procesar")
        return self.processor.fetch(self.filters)

    def revert(self) -> None:
        """
        Revierte las operaciones realizadas por este paso.
        Por defecto no realiza ninguna acción.
        """
        pass