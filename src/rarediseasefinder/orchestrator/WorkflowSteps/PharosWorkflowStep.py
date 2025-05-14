from ...biodata_providers.pharos.PharosProcessor import PharosProcessor
from ...orchestrator.IWorkflowStep import IWorkflowStep


class PharosWorkflowStep(IWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de Pharos.
    Este paso recupera datos biológicos desde Pharos basándose en los filtros proporcionados.
    """
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Pharos con valores predeterminados.
        """
        self.name = "Pharos step"
        self.description = "Fetches x data from Pharos API"
        self.processor = PharosProcessor()

    def set_filters(self, filters):
        """
        Establece los filtros para la consulta a Pharos.
        
        Args:
            filters: Los filtros a aplicar en la consulta.
        """
        self.filters = filters

    def get_status_code(self)->int:
        """
        Obtiene el código de estado de la última solicitud realizada.
        
        Returns:
            int: Código de estado HTTP.
        """
        return self.processor.get_status_code()

    def process(self)-> dict:
        """
        Procesa la consulta a Pharos utilizando los filtros configurados.
        
        Returns:
            dict: Resultados de la consulta a Pharos.
        """
        return self.processor.fetch(self.filters)

    def revert(self):
        """
        Revierte las operaciones realizadas por este paso.
        Actualmente no implementa ninguna acción.
        """
        pass