
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.rarediseasefinder.core.BaseScraper import BaseScraper
from src.rarediseasefinder.core.utils import get_unique_directory


class SelleckchemScrapper(BaseScraper):
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
        Inicializa el objeto SelleckchemScrapper.
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

    def buscar_medicamento(self,termino):
        """
        Busca un medicamento en la web de Selleckchem y devuelve el HTML de los resultados.

        Args:
            termino (str): Nombre o término a buscar.

        Returns:
            str or None: HTML de la página de resultados o None si ocurre un error.
        """
        try:
            self.driver.get(self.SELLECKCHEM_URL)
            search_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "searchDTO.searchParam"))
            )
            search_box.clear()
            search_box.send_keys(termino + Keys.RETURN)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr[name='productList']"))
            )
            html = self.driver.page_source
            self.driver.quit()
            return html
        except Exception as e:
            print("❌ Error:", e)
            self.driver.quit()
            return None

    def _ping_logic(self) -> int:
        if not self.ok:
            return 1001 # Error del scrapper al iniciar el driver 
        if self._try_connection(self.SELLECKCHEM_URL):
            response = SelleckchemScrapper._fetch_response(self.SELLECKCHEM_URL)
            return response.status_code
        else:
            return 999
        
    def check_data(self):
        pass  