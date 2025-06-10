from ...biodata_providers.pantherdb.PantherProcessor import PantherProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class PantherdbWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de Pantherdb.
    Este paso recupera datos biológicos desde Pantherdb basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Panther con valores predeterminados.
        """
        super().__init__(
            name="Panther step",
            description="Fetches x data from Panther API",
            processor=PantherProcessor()
        )