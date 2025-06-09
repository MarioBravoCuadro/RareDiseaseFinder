from typing import Dict

from ...core.BaseProcessor import BaseProcessor
from .DrugCentralScraper import DrugCentralScraper
from .DrugCentralParser import DrugCentralParser


class DrugCentralProcessor(BaseProcessor):
    """
    Processor para coordinar la obtención y transformación de datos de DrugCentral.
    """
    
    def __init__(self):
        """
        Inicializa el processor de DrugCentral con el scraper y el parser apropiados.
        """
        scraper = DrugCentralScraper()
        parser = DrugCentralParser()
        super().__init__(scraper, parser)
    
    def get_method_map(self) -> Dict[str, str]:
        """
        Obtiene un diccionario que mapea claves de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Mapeo de filtros a métodos.
        """
        return {
            "drug_results": "parse_drug_results"
        }