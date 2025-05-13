from typing import Dict
import json

from src.rarediseasefinder.biodata_providers.stringdb.StringDbClient import StringDbClient
from src.rarediseasefinder.biodata_providers.stringdb.StringDbParser import StringDbParser
from src.rarediseasefinder.core.BaseProcessor import BaseProcessor


class StringDbProcessor(BaseProcessor):

    def __init__(self):
        self.client = StringDbClient()
        self.parser = StringDbParser()
        super().__init__(self.client, self.parser)

    def get_method_map(self) -> Dict[str, str]:
        return {
            "get_annotation" : "get_annotation"
        }