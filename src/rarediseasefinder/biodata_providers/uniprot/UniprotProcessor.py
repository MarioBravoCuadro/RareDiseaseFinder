"""Módulo para procesar datos de UniProt combinando cliente y parser."""

from typing import Dict

from .UniProtClient import UniProtClient
from .UniProtParser import UniProtParser
from ...core.BaseProcessor import BaseProcessor


class UniprotProcessor(BaseProcessor):
    """Procesa datos de UniProt usando UniProtClient y UniProtParser."""

    def __init__(self):
        """Inicializa el cliente y el parser, y configura la clase base de procesamiento."""
        self.client = UniProtClient()
        self.parser = UniProtParser()
        super().__init__(self.client,self.parser)

    def get_method_map(self) -> Dict[str, str]:
        """Devuelve el mapeo de filtros a nombres de métodos de parseo."""
        return {
            "function": "parse_function",
            "subcellular_location": "parse_subcellular_location",
            "go_terms": "parse_go_terms",
            "disease": "parse_disease",
            "disease_publications": "parse_disease_publications",
            "interactions": "parse_interactions"
        }