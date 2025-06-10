from ...biodata_providers.drugcentral.DrugCentralProcessor import DrugCentralProcessor
from .BaseWorkflowStep import BaseWorkflowStep


class DrugCentralWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo para obtener y procesar datos de medicamentos desde DrugCentral.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de DrugCentral con valores predeterminados.
        """
        super().__init__(
            name="DrugCentral step",
            description="Fetches drug information data from DrugCentral database",
            processor=DrugCentralProcessor()
        )