from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class UniprotWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de Uniprot.
    Este paso recupera datos de proteínas desde Uniprot basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Uniprot con valores predeterminados.
        """
        super().__init__(
            name="Uniprot step",
            description="Fetches protein data from Uniprot API",
            processor=UniprotProcessor()
        )