import pandas as pd

from src.rarediseasefinder.core.BaseParser import BaseParser


class PantherParser(BaseParser):
    """
    Parser para datos obtenidos de PantherDB.
    Esta clase implementa métodos para extraer y formatear información específica de los datos
    de PantherDB.
    """

    def __init__(self):
        """
        Inicializa una instancia del parser de PantherDB.
        """
        super().__init__()

    def get_annotation_name(self, data:dict) -> pd.DataFrame:
        """
        Extrae el nombre de la anotación de los datos proporcionados por PantherDB.
        
        Args:
            data (dict): Datos obtenidos de la API de PantherDB.
            
        Returns:
            pd.DataFrame: DataFrame con el nombre de la anotación.
        """
        # Obtener la lista de annotations
        annotations = data['search']['mapped_genes']['gene']['annotation_type_list']['annotation_data_type']
        # Verificar que hay al menos 2 elementos (índice 1)
        if len(annotations) > 1:
            # Obtener el nombre de la annotation en la posición 1
            annotation_name = [annotations[1]['annotation_list']['annotation']['name']]
            annotation_name = {annotation_name[0]:""}
            return self.parse_to_dataframe(annotation_name)

        else: return self.parse_to_dataframe([""])