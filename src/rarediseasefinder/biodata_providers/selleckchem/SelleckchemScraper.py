"""
Módulo de scrapper para automatizar búsquedas en Selleckchem usando Selenium.
Proporciona una clase para buscar medicamentos y obtener el HTML de resultados.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Dict, Any
import re

from ...core.BaseScraper import BaseScraper


class SelleckchemScraper(BaseScraper):
    """
    Clase para automatizar la búsqueda de medicamentos en Selleckchem usando Selenium.
    Proporciona la función buscar_medicamento para obtener el HTML de los resultados
    de búsqueda de un término dado en la web de Selleckchem.
    """

    def __init__(self):
        """
        Inicializa el objeto SelleckchemScraper.
        """
        super().__init__("https://www.selleckchem.com/search.html")

    def fetch(self, id: str) -> Dict[str, Any]:
        """
        Busca un medicamento en la web de Selleckchem y devuelve el HTML de los resultados.

        Args:
            id (str): identificador del medicamento a buscar. Generalmente un nombre o ID de producto.

        Returns:
            Dict[str, Any]: HTML de la página de resultados o mensaje de error.
        """
        if not self.ok():
            return {"error": "Error al inicializar Chrome driver"}
        if self._is_iupac_name(id):
            return {"error": "No se permiten nombres IUPAC"}
        try:
            self.driver.get(self.BASE_URL)
            search_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "searchDTO.searchParam"))
            )
            search_box.clear()
            search_box.send_keys(id + Keys.RETURN)
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr[name='productList']"))
            )
            html = self.driver.page_source
            return {"html": html, "search_term": id}
        except Exception as e:
            print(f"❌ Error al buscar en Selleckchem: {str(e)}")
            self.reset_driver()
            return {"error": str(e)}
    
    def _is_iupac_name(self, product_name: str) -> bool:
        """
        Detecta si un nombre de producto parece nomenclatura IUPAC.
        Con que coincida con algún patrón típico, se considera IUPAC.
        
        Args:
            product_name (str): Nombre del producto a evaluar
            
        Returns:
            bool: True si parece ser nomenclatura IUPAC, False en caso contrario
        """
        if not product_name or product_name == "N/A":
            return False
        # Patrones comunes de nomenclatura IUPAC
        iupac_patterns = [
            r'^\d+',      # Comienza con número: 5-(naphthalen...), 2-(2,4-dichlorophenoxy)...
            r'^\(',       # Comienza con paréntesis: (R)-2-amino..., (±)-compound...
            r'-',         # Contiene guión: methyl-2-chloride, N-acetyl, 2,4-dichloro...
        ]
        
        for pattern in iupac_patterns:
            if re.search(pattern, product_name, re.IGNORECASE):
                return True
        
        return False