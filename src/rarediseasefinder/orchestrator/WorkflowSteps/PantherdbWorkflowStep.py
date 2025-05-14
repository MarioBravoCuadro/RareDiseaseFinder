from src.rarediseasefinder.biodata_providers.phanterdb.PhanterProcessor import PhanterProcessor
from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep


class PantherdbWorkflowStep(IWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de Pantherdb.
    Este paso recupera datos biológicos desde Pantherdb basándose en los filtros proporcionados.
    """
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Panther con valores predeterminados.
        """
        self.name = "Panther step"
        self.description = "Fetches x data from Panther API"
        self.processor = PhanterProcessor()

    def set_filters(self, filters):
        """
        Establece los filtros para la consulta a Pantherdb.
        
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
        Procesa la consulta a Pantherdb utilizando los filtros configurados.
        
        Returns:
            dict: Resultados de la consulta a Pantherdb.
        """
        return self.processor.fetch(self.filters)

    def revert(self):
        """
        Revierte las operaciones realizadas por este paso.
        Actualmente no implementa ninguna acción.
        """
        pass