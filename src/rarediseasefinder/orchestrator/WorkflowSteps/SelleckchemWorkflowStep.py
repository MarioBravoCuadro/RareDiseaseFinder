from ...biodata_providers.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class SelleckchemWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo que interactúa con Selleckchem.
    Este paso extrae información de medicamentos desde Selleckchem basándose en los filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de Selleckchem con valores predeterminados.
        """
        super().__init__(
            name="Selleckchem step",
            description="Gets links from selleckchem for any drug term",
            processor=SelleckchemProcessor()
        )