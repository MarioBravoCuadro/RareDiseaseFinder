"""
Módulo para gestionar la extracción de datos de DrugCentral mediante web scraping.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Dict, Any

from ...core.BaseScraper import BaseScraper


class DrugCentralScraper(BaseScraper):
    """
    Scraper para extraer información de medicamentos de DrugCentral.
    """
    
    def __init__(self):
        """
        Inicializa el scraper de DrugCentral.
        """
        super().__init__("https://drugcentral.org")
    
    def fetch(self, id: str) -> Dict[str, Any]:
        """
        Busca un término en DrugCentral y devuelve el HTML de los resultados.
        
        Args:
            id (str): Identificador para la búsqueda (proteína, gen, etc.)
        
        Returns:
            Dict[str, Any]: HTML de resultados o mensaje de error
        """
        if not self.ok():
            return {"error": "Error al inicializar Chrome driver"}
            
        try:
            search_url = f"{self.BASE_URL}/?q={id}"
            self.driver.get(search_url)
            
            # Esperar a que cargue la tabla de resultados o un mensaje de no resultados
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(By.TAG_NAME, "table") or 
                          d.find_element(By.XPATH, "//div[contains(text(), 'No results found')]")
            )
            
            html = self.driver.page_source
            return {"html": html, "search_term": id}
                
        except Exception as e:
            print(f"❌ Error al buscar en DrugCentral: {str(e)}")
            self.reset_driver()
            return {"error": str(e)}
    
    def fetch_drug_details(self, drug_id: str, search_term: str) -> Dict[str, Any]:
        """
        Obtiene detalles adicionales de un medicamento específico.
        
        Args:
            drug_id (str): ID del medicamento en DrugCentral
            search_term (str): Término original de búsqueda
            
        Returns:
            Dict[str, Any]: HTML con detalles del medicamento
        """
        if not self.ok():
            return {"error": "Error al inicializar Chrome driver"}
            
        try:
            detail_url = f"{self.BASE_URL}/drugcard/{drug_id}?q={search_term}"
            self.driver.get(detail_url)
            
            # Esperar a que cargue la información del medicamento
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "card-title"))
            )
            
            html = self.driver.page_source
            return {"html": html, "drug_id": drug_id}
                
        except Exception as e:
            print(f"❌ Error al obtener detalles del medicamento: {str(e)}")
            self.reset_driver()
            return {"error": str(e)}