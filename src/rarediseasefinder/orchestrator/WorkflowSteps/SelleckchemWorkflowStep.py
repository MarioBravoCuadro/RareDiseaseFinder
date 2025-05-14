from ...biodata_providers.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from ...orchestrator.IWorkflowStep import IWorkflowStep


class SelleckchemWorkflowStep(IWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con Selleckchem.
    Este paso extrae información de medicamentos desde Selleckchem basándose en los filtros proporcionados.
    """
    name = None
    description = None
    processor = None
    filters = None

    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Selleckchem con valores predeterminados.
        """
        self.name = "Selleckchem step"
        self.description = "Gets links from selleckchem for x term"
        self.processor = SelleckchemProcessor()

    def set_filters(self, filters):
        """
        Establece los filtros para la búsqueda en Selleckchem.
        
        Args:
            filters: Los filtros a aplicar en la búsqueda.
        """
        self.filters = filters

    def get_status_code(self)->int:
        """
        Obtiene el código de estado de la última solicitud realizada.
        
        Returns:
            int: Código de estado HTTP.
        """
        return self.processor.get_status_code()

    def process(self)->dict:
        """
        Procesa la búsqueda en Selleckchem utilizando los filtros configurados.
        
        Returns:
            dict: Resultados de la búsqueda en Selleckchem.
        """
        return self.processor.fetch(self.filters)

    def revert(self):
        """
        Revierte las operaciones realizadas por este paso.
        Actualmente no implementa ninguna acción.
        """
        pass