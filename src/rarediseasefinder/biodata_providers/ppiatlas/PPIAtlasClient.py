import json
import requests
from typing import Dict, Any

from ...core.BaseClient import BaseClient


class PPIAtlasClient(BaseClient):
    """
    Cliente para la API de PPIAtlas que permite obtener interacciones proteína-proteína.
    """

    BASE_URL = "https://www.ppiatlas.com/api"
    
    def __init__(self):
        """
        Inicializa una instancia del cliente de PPIAtlas.
        """
        super().__init__()

    def fetch(self, id: str) -> Dict[str, Any]:
        """
        Obtiene datos de interacciones proteína-proteína de PPIAtlas.
        
        Args:
            id (str): Identificador de la proteína.
            
        Returns:
            Dict[str, Any]: Datos obtenidos de PPIAtlas.
        """
        # Crear URL para la consulta
        url = f"{self.BASE_URL}/stream-scores/{id}?limit=99999999999"
        
        try:
            # Hacer petición HTTP con streaming
            response = self._http_response(url, stream=True)
            response.raise_for_status()
            
            # Procesar la respuesta de streaming
            records = []
            for line in response.iter_lines():
                if line.startswith(b'data: '):
                    json_str = line[len(b'data: '):]
                    try:
                        record = json.loads(json_str)
                        records.append(record)
                    except json.JSONDecodeError:
                        continue  # Ignora líneas mal formateadas
            return {"records": records}

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def _ping_logic(self) -> int:
        """
        Verifica si el servicio de PPIAtlas está funcionando.
        
        Returns:
            int: Código de estado de la respuesta HTTP o 999 si no hay conexión.
        """
        url = f"{self.BASE_URL}/stream-scores/TP53?limit=1"
        if self._try_connection(url):
            response = self._http_response(url)
            return response.status_code
        else:
            return 999
        
    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos de PPIAtlas.
        """
        pass