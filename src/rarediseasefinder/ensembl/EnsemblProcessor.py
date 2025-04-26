from .EnsemblClient import EnsemblClient
from .EnsemblParser import EnsemblParser

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

    def get_ensembl_id(self, genTerm:str)-> str | None:
        """
        Obtiene el identificador Ensembl de un gen dado su nombre.
        Args:
            genTerm (str): Nombre del gen a consultar.
        Returns:
            str or None: Identificador Ensembl si se encuentra, None en caso contrario.
        """
        data = self.ensembl_client.get_by_gene(genTerm)
        if data:
            ensembl_id = self.ensembl_parser.parse_id(data)
            return ensembl_id
        else:
            return None

    #TODO implementar consulta al cliente mediante un ping a la url de este
    def getStatus(self) -> str:
        return "OK"