from src.rarediseasefinder.biodata_providers.stringdb.StringDbProcessor import StringDbProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class StringdbWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de StringDB.
    Este paso recupera datos de interacciones de proteínas desde StringDB basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de StringDB con valores predeterminados.
        """
        super().__init__(
            name="Stringdb step",
            description="Fetches protein-protein interaction data from Stringdb API",
            processor=StringDbProcessor()
        )