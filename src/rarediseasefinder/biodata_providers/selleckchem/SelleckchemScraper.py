"""
Módulo de scrapper para automatizar búsquedas en Selleckchem usando Selenium.
Proporciona una clase para buscar medicamentos y obtener el HTML de resultados.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.rarediseasefinder.core.BaseScraper import BaseScraper
from src.rarediseasefinder.core.utils import get_unique_directory


class SelleckchemScraper(BaseScraper):
    """
    Clase para automatizar la búsqueda de medicamentos en Selleckchem usando Selenium.
    Proporciona la función buscar_medicamento para obtener el HTML de los resultados
    de búsqueda de un término dado en la web de Selleckchem.
    """
    chrome_options = None
    unique_dir = None
    driver = None

    SELLECKCHEM_URL = "https://www.selleckchem.com/search.html"

    def __init__(self):
        """
        Inicializa el objeto SelleckchemScraper.
        """
        super().__init__()
        self.unique_dir = get_unique_directory()
        self.chrome_options = self.getOptionsChromeDriver()
        self.chrome_options.add_argument(f"--user-data-dir={self.unique_dir}")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def __del__(self):
        """
        Destructor para cerrar el navegador al eliminar la instancia.
        """
        if self.driver:
            self.driver.quit()

    def fetch(self,id:str) -> dict:
        """
        Busca un medicamento en la web de Selleckchem y devuelve el HTML de los resultados.

        Args:
            id (str): identificador del medicamento a buscar. Generalmente un nombre o ID de producto.

        Returns:
            str or None: HTML de la página de resultados o None si ocurre un error.
        """
        try:
            self.driver.get(self.SELLECKCHEM_URL)
            search_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "searchDTO.searchParam"))
            )
            search_box.clear()
            search_box.send_keys(id + Keys.RETURN)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr[name='productList']"))
            )
            html = self.driver.page_source
            self.driver.quit()
            return {"html": html}
        except Exception as e:
            print("❌ Error:", e)
            self.driver.quit()
            return {"error": str(e)}

    def _ping_logic(self) -> int:
        """
        Comprueba la accesibilidad de la web de Selleckchem.

        Returns:
            int: Código de estado HTTP de la página, 1001 si falla el driver o 999 si no hay conexión.
        """
        if not self.ok:
            return 1001
        if self._try_connection(self.SELLECKCHEM_URL):
            response = SelleckchemScraper._http_response(self.SELLECKCHEM_URL)
            return response.status_code
        else:
            return 999
        
    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos con Selenium.

        Raises:
            NotImplementedError: Indica que el método no está implementado.
        """
        pass