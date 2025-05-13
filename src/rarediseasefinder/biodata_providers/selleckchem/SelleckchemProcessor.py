from typing import Dict

from ..selleckchem import SelleckchemParser
from ..selleckchem import SelleckchemScraper
from ...core.BaseProcessor import BaseProcessor

class SelleckchemProcessor(BaseProcessor):
    """
    Procesa datos de Selleckchem usando SelleckchemScrapper y SelleckchemParser.
    Obtiene enlaces de productos de un medicamento según filtros.
    """
    def __init__(self):
        """
        Inicializa el procesador de Selleckchem.
        Configura el scrapper, el parser y el mapeo de métodos.
        """
        self.client = SelleckchemScraper.SelleckchemScraper()
        self.parser = SelleckchemParser.SelleckchemParser()
        super().__init__(self.client,self.parser)

    def get_method_map(self) -> Dict[str, str]:
        """
        Retorna un mapeo de filtros a nombres de métodos del parser.

        Returns:
            Dict[str, str]: Claves de filtros y métodos asociados.
        """
        return {
            "obtener_link_selleckchem": "obtener_link_selleckchem",
            "obtener_links_selleckchem": "obtener_links_selleckchem"
        }