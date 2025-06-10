from ...biodata_providers.ensembl.EnsemblProcessor import EnsemblProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class EnsemblerWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de Ensembl.
    Este paso recupera datos genómicos desde Ensembl basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Ensembl con valores predeterminados.
        """
        super().__init__(
            name="Ensembl step",
            description="Fetches data from Ensembl API",
            processor=EnsemblProcessor()
            )