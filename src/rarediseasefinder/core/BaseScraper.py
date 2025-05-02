from selenium.webdriver.chrome.options import Options
from ..core.BaseRetriever import BaseRetriever
from abc import ABC, abstractmethod


class BaseScraper(BaseRetriever, ABC):
    def __init__(self):
        pass
    #TODO implementar firefox driver también

    def getOptionsChromeDriver(self):
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