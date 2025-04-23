from ..selleckchem import SelleckchemScrapper
from ..selleckchem import SelleckchemParser

class SelleckchemProcessor:
    """Clase processor para interactuar con la API de Selleckchem.
    Esta clase permite buscar medicamentos y obtener información relevante.
    """
    scrapper = None
    parser = None

    def __init__(self):
        self.scrapper = SelleckchemScrapper.SelleckchemScrapper()
        self.parser = SelleckchemParser.SelleckchemParser()
        
    def obtener_link_selleckchem(self,farmaco):
        """Obtiene el primer link relevante de Selleckchem para un fármaco
        Args:
            farmaco (str): Nombre del fármaco a buscar.
        Returns:
            str: Primer link relevante de Selleckchem para el fármaco    
        """
        try:
            html = self.scrapper.buscar_medicamento(farmaco)
            if not html:
                return None
            productos = self.parser.extraer_medicamentos(html)
            if not productos.empty:
                primer_link = f"www.selleckchem.com{productos.loc[0]['Link']}"
                return primer_link
            return None
        except Exception as e:
            print(f"Error obteniendo {farmaco}: {str(e)}")
            return None
        
    def obtener_links_selleckchem(self,farmaco):
        """Obtiene todos los links relevantes de Selleckchem para un fármaco
        Args:
            farmaco (str): Nombre del fármaco a buscar. 
        Returns:
            list: Lista de links relevantes de Selleckchem para el fármaco  
        """
        try:
            html = self.scrapper.buscar_medicamento(farmaco)
            if not html:
                return None
            productos = self.parser.extraer_medicamentos(html)

            links = []
            rango = range(len(productos))
            for i in rango:
                links.append(f"www.selleckchem.com{productos.loc[i]['Link']}")

            links = self.parser.parse_to_dataframe(links)
            return links
        except Exception as e:
            print(f"Error obteniendo {farmaco}: {str(e)}")
            return None