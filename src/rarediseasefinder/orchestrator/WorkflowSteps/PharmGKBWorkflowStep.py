from ...biodata_providers.pharmgkb.PharmGKBProcessor import PharmGKBProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class PharmGKBWorkflowStep(BaseWorkflowStep):
    """
    Paso de workflow que interactúa con la API de PharmGKB.
    Este paso recupera datos biológicos desde PharmGKB basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de workflow de PharmGKB.
        """
        super().__init__(
            name="PharmGKB step",
            description="Fetches biological data from PharmGKB API",
            processor=PharmGKBProcessor()
        )
