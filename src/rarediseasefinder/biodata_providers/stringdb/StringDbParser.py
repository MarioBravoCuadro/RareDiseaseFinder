import pandas as pd

from src.rarediseasefinder.biodata_providers.stringdb.StringDbClient import StringDbClient
from src.rarediseasefinder.core.BaseParser import BaseParser


class StringDbParser(BaseParser):
    def __init__(self):
        super().__init__()

    def get_annotation(self,data:dict)->pd.DataFrame:

        name = data[0].get("preferredName", "")
        description = data[0].get("annotation", "")
        result = {"Prefered name" : name, "Annotation" : description}
        return self.parse_to_dataframe(result)