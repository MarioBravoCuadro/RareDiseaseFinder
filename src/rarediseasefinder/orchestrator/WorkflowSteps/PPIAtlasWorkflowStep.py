from ...biodata_providers.ppiatlas.PPIAtlasProcessor import PPIAtlasProcessor
from .BaseWorkflowStep import BaseWorkflowStep

class PPIAtlasWorkflowStep(BaseWorkflowStep):
    """
    Paso de flujo de trabajo para obtener y procesar datos de interacciones proteína-proteína desde PPIAtlas.
    """
    def __init__(self):
        """
        Inicializa el paso de flujo de trabajo de PPIAtlas con valores predeterminados.
        """
        super().__init__(
            name="PPIAtlas step",
            description="Fetches protein-protein interaction data from PPIAtlas API",
            processor=PPIAtlasProcessor()
        )