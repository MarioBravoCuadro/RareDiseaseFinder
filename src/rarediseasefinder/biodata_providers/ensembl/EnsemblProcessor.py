from .EnsemblClient import EnsemblClient
from .EnsemblParser import EnsemblParser
import pandas as pd
from typing import Optional

class EnsemblProcessor:
    """
    Clase para procesar datos de Ensembl utilizando EnsemblClient y EnsemblParser.
    Permite obtener el identificador Ensembl de un gen dado su nombre.
    """
    ensembl_client = None
    ensembl_parser = None

    def __init__(self):
        """
        Inicializa el procesador creando instancias de EnsemblClient y EnsemblParser.
        """
        self.ensembl_client = EnsemblClient()
        self.ensembl_parser = EnsemblParser()

    def get_ensembl_id(self, genTerm: str) -> Optional[str]:
        """
        Obtiene el identificador Ensembl de un gen dado su nombre.
        
        Args:
            genTerm (str): Nombre del gen a consultar.
            
        Returns:
            Optional[str]: Identificador Ensembl si se encuentra, None en caso contrario.
        """
        data = self.ensembl_client.get_by_gene(genTerm)
        if data:
            # Ahora parse_id devuelve un DataFrame
            ensembl_id_df = self.ensembl_parser.parse_id(data)
            # Extraer el valor del identificador del DataFrame
            if not ensembl_id_df.empty and "ID" in ensembl_id_df.columns:
                return ensembl_id_df["ID"].iloc[0]
        return None

    #TODO implementar consulta al cliente mediante un ping a la url de este
    def getStatus(self) -> str:
        return "OK"