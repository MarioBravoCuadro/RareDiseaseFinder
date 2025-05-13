import json
from typing import Dict

from src.rarediseasefinder.biodata_providers.phanterdb.PhanterClient import PhanterClient
from src.rarediseasefinder.biodata_providers.phanterdb.PhanterParser import PhanterParser
from src.rarediseasefinder.core.BaseProcessor import BaseProcessor


class PhanterProcessor(BaseProcessor):
    def __init__(self):
        self.client = PhanterClient()
        self.parser = PhanterParser()
        super().__init__(self.client, self.parser)

    def get_method_map(self) -> Dict[str, str]:
        return {
            "annotation_name": "get_annotation_name",
        }