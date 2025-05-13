from email.utils import parsedate_to_datetime
from xml.sax import parse

import pandas as pd

from src.rarediseasefinder.core.BaseParser import BaseParser


class PhanterParser(BaseParser):

    def __init__(self):
        super().__init__()

    def get_annotation_name(self, data:dict) -> pd.DataFrame:
        # Obtener la lista de annotations
        annotations = data['search']['mapped_genes']['gene']['annotation_type_list']['annotation_data_type']
        # Verificar que hay al menos 2 elementos (índice 1)
        if len(annotations) > 1:
            # Obtener el nombre de la annotation en la posición 1
            annotation_name = [annotations[1]['annotation_list']['annotation']['name']]
            annotation_name = {annotation_name[0]:""}
            return self.parse_to_dataframe(annotation_name)

        else: return self.parse_to_dataframe([""])