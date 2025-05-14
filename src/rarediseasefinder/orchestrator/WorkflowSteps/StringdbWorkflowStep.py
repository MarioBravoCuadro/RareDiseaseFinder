from src.rarediseasefinder.biodata_providers.stringdb.StringDbProcessor import StringDbProcessor
from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep


class StringdbWorkflowStep(IWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de StringDB.
    Este paso recupera datos de interacciones de proteínas desde StringDB basándose en los filtros proporcionados.
    """
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de StringDB con valores predeterminados.
        """
        self.name = "Stringdb step"
        self.description = "Fetches x data from Stringdb API"
        self.processor = StringDbProcessor()

    def set_filters(self, filters):
        """
        Establece los filtros para la consulta a StringDB.
        
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
        Procesa la consulta a StringDB utilizando los filtros configurados.
        
        Returns:
            dict: Resultados de la consulta a StringDB.
        """
        return self.processor.fetch(self.filters)

    def revert(self):
        """
        Revierte las operaciones realizadas por este paso.
        Actualmente no implementa ninguna acción.
        """
        pass