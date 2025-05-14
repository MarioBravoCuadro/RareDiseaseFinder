from src.rarediseasefinder.biodata_providers.opentargets.OpenTargetsProcessor import OpenTargetsProcessor
from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep


class OpentargetsStep(IWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de OpenTargets.
    Este paso recupera datos biológicos desde OpenTargets basándose en los filtros proporcionados.
    """
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de OpenTargets con valores predeterminados.
        """
        self.name = "OpenTargets step"
        self.description = "Fetches x data from OpenTargets API"
        self.processor = OpenTargetsProcessor()

    def set_filters(self, filters):
        """
        Establece los filtros para la consulta a OpenTargets.
        
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
        Procesa la consulta a OpenTargets utilizando los filtros configurados.
        
        Returns:
            dict: Resultados de la consulta a OpenTargets.
        """
        return self.processor.fetch(self.filters)

    def revert(self):
        """
        Revierte las operaciones realizadas por este paso.
        Actualmente no implementa ninguna acción.
        """
        pass