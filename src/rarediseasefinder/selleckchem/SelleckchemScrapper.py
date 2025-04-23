
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..core.utils import get_unique_directory
from ..core.scraper import Scraper

class SelleckchemScrapper(Scraper):
    """
    Clase para automatizar la búsqueda de medicamentos en Selleckchem usando Selenium.
    Proporciona la función buscar_medicamento para obtener el HTML de los resultados
    de búsqueda de un término dado en la web de Selleckchem.
    """
    chrome_options = None
    unique_dir = None
    driver = None


    def __init__(self):
        """
        Inicializa el objeto SelleckchemScrapper.
        """
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
            self.driver.get("https://www.selleckchem.com/search.html")
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