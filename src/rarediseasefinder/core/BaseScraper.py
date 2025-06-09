
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Dict, Any

from ..core.BaseRetriever import BaseRetriever
from ..core.utils import get_unique_directory


class BaseScraper(BaseRetriever, ABC):
    """
    Clase abstracta que extiende BaseRetriever y define la configuración básica de un scraper.
    """
    def __init__(self, base_url: str):
        """
        Inicializa la instancia de BaseScraper.
        
        Args:
            base_url (str): URL base del sitio a scrapear
        """
        self.BASE_URL = base_url
        self.unique_dir = get_unique_directory()
        self.chrome_options = self.getOptionsChromeDriver()
        self.chrome_options.add_argument(f"--user-data-dir={self.unique_dir}")
        
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except Exception as e:
            print(f"Error al inicializar Chrome: {e}")
            self.driver = None

    def __del__(self):
        """
        Destructor para cerrar el navegador al eliminar la instancia.
        """
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def getOptionsChromeDriver(self) -> Options:
        """
        Configura y devuelve las opciones para instanciar ChromeDriver con Selenium.

        Returns:
            Options: Configuración de opciones de ChromeDriver.
        """
        # Configuración de Chrome
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        options.add_argument("--headless")
        options.add_argument("--verbose")

        return options
    
    def ok(self) -> bool:
        """
        Indica si el scraper está listo para operar.

        Returns:
            bool: True si está listo, False en caso contrario.
        """
        return hasattr(self, 'driver') and self.driver is not None
    
    def _ping_logic(self) -> int:
        """
        Verifica la disponibilidad del sitio.
        
        Returns:
            int: Código de estado HTTP si la conexión es exitosa, 999 si falla,
                 1001 si hay un error con el driver.
        """
        if not self.ok():
            return 1001
            
        if self._try_connection(self.BASE_URL):
            response = self._http_response(self.BASE_URL)
            return response.status_code
        else:
            return 999
    
    def reset_driver(self):
        """
        Reinicia el driver en caso de error.
        """
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
        
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except Exception as e:
            print(f"Error al reiniciar Chrome: {e}")
            self.driver = None
    
    @abstractmethod
    def fetch(self, id: str) -> Dict[str, Any]:
        """
        Método abstracto para buscar y obtener datos.
        Debe ser implementado por las clases hijas.
        
        Args:
            id (str): Identificador para la búsqueda
            
        Returns:
            Dict[str, Any]: Datos obtenidos o mensaje de error
        """
        pass
    
    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos.
        """
        pass