from ...biodata_providers.guidetopharmacology.PharmacologyProcessor import PharmacologyProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class PharmacologyWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de Pharmacology.
    Este paso recupera datos biológicos desde Pharmacology basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Pharmacology con valores predeterminados.
        """
        super().__init__(
            name="Pharmacology step",
            description="Fetches biological data from Pharmacology API",
            processor=PharmacologyProcessor()
        )