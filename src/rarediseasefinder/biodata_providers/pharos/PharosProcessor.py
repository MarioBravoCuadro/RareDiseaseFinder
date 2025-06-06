from typing import Dict

from .PharosClient import PharosClient
from .PharosParser import PharosParser
from ...core.BaseProcessor import BaseProcessor


class PharosProcessor(BaseProcessor):
    """
    Procesa datos de Pharos mediante PharosClient y PharosParser.
    Obtiene datos de un objetivo y los convierte en DataFrames según filtros proporcionados.
    """
    def __init__(self):
        """
        Inicializa el procesador de Pharos.
        Configura el cliente, el parser y el mapeo de métodos.
        """
        self.client = PharosClient()
        self.parser = PharosParser()
        super().__init__(self.client,self.parser)

    def get_method_map(self) -> Dict[str, str]:
        """
        Obtiene un diccionario que mapea claves de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Mapeo de filtros a métodos.
        """
        return {
            "df_info": "create_info_df",
            "df_omim": "create_omim_df",
            "create_protein_protein_relations_df": "create_protein_protein_relations_df",
            "df_numero_vias_por_fuente": "create_numero_vias_por_fuente_df",
            "df_vias": "create_vias_df",
            "Metodo prueba": "create_vias_df"

        }
