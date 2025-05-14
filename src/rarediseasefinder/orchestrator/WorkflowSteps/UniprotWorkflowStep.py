from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor
from src.rarediseasefinder.orchestrator.IWorkflowStep import IWorkflowStep


class UniprotWorkflowStep(IWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de Uniprot.
    Este paso recupera datos de proteínas desde Uniprot basándose en los filtros proporcionados.
    """
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Uniprot con valores predeterminados.
        """
        self.name = "Uniprot step"
        self.description = "Fetches x data from Uniprot API"
        self.processor = UniprotProcessor()

    def set_filters(self, filters):
        """
        Establece los filtros para la consulta a Uniprot.
        
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
        Procesa la consulta a Uniprot utilizando los filtros configurados.
        
        Returns:
            dict: Resultados de la consulta a Uniprot.
        """
        return self.processor.fetch(self.filters)

    def revert(self):
        """
        Revierte las operaciones realizadas por este paso.
        Actualmente no implementa ninguna acción.
        """
        pass