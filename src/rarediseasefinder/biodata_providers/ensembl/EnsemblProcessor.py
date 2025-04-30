import pandas as pd

from ...core.BaseProcessor import BaseProcessor
from .EnsemblClient import EnsemblClient
from .EnsemblParser import EnsemblParser
from typing import Optional, Dict

class EnsemblProcessor(BaseProcessor):
    """
    Clase para procesar datos de Ensembl utilizando EnsemblClient y EnsemblParser.
    Permite obtener el identificador Ensembl de un gen dado su nombre.
    """
    
    def __init__(self):
        """
        Inicializa el procesador creando instancias de EnsemblClient y EnsemblParser.
        """
        super().__init__()
        self.client = EnsemblClient()
        self.parser = EnsemblParser()

    def get_ensembl_id(self, genTerm: str) -> Optional[str]:
        """
        Obtiene el identificador Ensembl de un gen dado su nombre.
        
        Args:
            genTerm (str): Nombre del gen a consultar.
            
        Returns:
            Optional[str]: Identificador Ensembl si se encuentra, None en caso contrario.
        """
        data = self.client.get_by_gene(genTerm)
        if data:
            # Ahora parse_id devuelve un DataFrame
            ensembl_id_df = self.parser.parse_id(data)
            # Extraer el valor del identificador del DataFrame
            if not ensembl_id_df.empty and "ID" in ensembl_id_df.columns:
                return ensembl_id_df["ID"].iloc[0]
        return None
        
    def fetch(self, filters: dict) -> Dict[str, pd.DataFrame]:
        """
        Obtiene todos los datos de Ensembl para un gen en formato DataFrame.
        
        Args:
            genTerm (str): Nombre del gen a consultar.
            
        Returns:
            pd.DataFrame: DataFrame con la información del gen o DataFrame vacío si no se encuentra.
        """
        search_params = self.client_filters(filters)
        if not search_params or "search_id" not in search_params:
            print("Error: No se encontró un search_id válido en los filtros")
            return {}
        search_id = search_params["search_id"]
        data = self.client.get_by_gene(search_id)
        if data:
            return self.parser.parse_id(data)
        return pd.DataFrame()