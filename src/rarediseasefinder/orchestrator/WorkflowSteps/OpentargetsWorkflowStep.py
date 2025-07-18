from ...biodata_providers.opentargets.OpenTargetsProcessor import OpenTargetsProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class OpentargetsWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con la API de OpenTargets.
    Este paso recupera datos biológicos desde OpenTargets basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de OpenTargets con valores predeterminados.
        """
        super().__init__(
            name="OpenTargets step",
            description="Fetches biological data from OpenTargets API",
            processor=OpenTargetsProcessor()
        )
