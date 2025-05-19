from ...biodata_providers.pharos.PharosProcessor import PharosProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class PharosWorkflowStep(BaseWorkflowStep):
    """
    Paso de workflow que interactúa con la API de Pharos.
    Este paso recupera datos biológicos desde Pharos basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de workflow de Pharos.
        """
        super().__init__(
            name="Pharos step",
            description="Fetches biological data from Pharos API",
            processor=PharosProcessor()
        )