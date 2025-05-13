from abc import ABC

from src.rarediseasefinder.core.BaseClient import BaseClient

#https://pantherdb.org/services/openAPISpec.jsp
class PhanterClient(BaseClient, ABC):

    PHANTER_DOMAIN_URL = f"https://pantherdb.org"
    PHANTER_SERVICE_URL = "/services/oai/pantherdb/geneinfo?geneInputList="""
    PHANTER_URL_SUFIX = "&organism=9606"

    def __init__(self):
        pass

    def _create_url_string(self,gen_term )-> str:
        return str(self.PHANTER_DOMAIN_URL + self.PHANTER_SERVICE_URL + gen_term + self.PHANTER_URL_SUFIX)

    def fetch(self,gen_term)->dict:
        url = self._create_url_string(gen_term)
        return self._get_data(url)

    def _ping_logic(self) -> int:
        #TODO Implement a better way to check if the service is up,
        url = self.PHANTER_DOMAIN_URL + self.PHANTER_SERVICE_URL
        if self._try_connection(url):
            response = self._http_response(url)
            return response.status_code
        else:
            return 999

    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos de Phanter.
        """
        pass