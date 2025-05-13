from src.rarediseasefinder.core.BaseClient import BaseClient


class StringDbClient(BaseClient):
    STRINGDB_PING_URL = "https://string-db.org/api/json/version"
    STRINGDB_BASE_URL = "https://string-db.org/api/json/get_string_ids?identifiers="
    def __init__(self):
        pass

    def create_url(self, id:str)->str:
        return str(self.STRINGDB_BASE_URL + id)

    def fetch(self,id: str) -> dict:
        return self._get_data(self.create_url(id))

    def _ping_logic(self) -> int:
        if self._try_connection(self.STRINGDB_PING_URL):
            response = self._http_response(self.STRINGDB_PING_URL)
            return response.status_code
        else:
            return 999

    def check_data(self, data: str | dict) -> bool:
        pass
