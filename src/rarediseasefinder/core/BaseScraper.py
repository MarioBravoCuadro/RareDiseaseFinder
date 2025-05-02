"""
BaseScraper.py

Clase base para scrapers utilizando Selenium con ChromeDriver.
"""

from abc import ABC

from selenium.webdriver.chrome.options import Options

from ..core.BaseRetriever import BaseRetriever


class BaseScraper(BaseRetriever, ABC):
    """
    Clase abstracta que extiende BaseRetriever y define la configuración básica de un scraper.
    """
    def __init__(self):
        """
        Inicializa la instancia de BaseScraper.
        """
        pass
    #TODO implementar firefox driver también

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
        return True