from typing import Dict, Any

from ...core.BaseClient import BaseClient


class PharmacologyClient(BaseClient):
    """
    Cliente para comunicarse con la API de Guide to Pharmacology.
    """
    
    BASE_URL = "https://www.guidetopharmacology.org/services"
    
    def __init__(self):
        """
        Inicializa el cliente de Guide to Pharmacology.
        """
        super().__init__()
    
    def _ping_logic(self) -> int:
        """
        Verifica la disponibilidad de la API de Guide to Pharmacology.
        
        Returns:
            int: Código de estado HTTP si la conexión es exitosa, 999 si falla.
        """
        if self._try_connection(f"{self.BASE_URL}/targets"):
            response = self._http_response(f"{self.BASE_URL}/targets")
            return response.status_code
        else:
            return 999
    
    def _create_url_string(self, endpoint: str) -> str:
        """
        Crea la URL de consulta para Guide to Pharmacology.
        
        Args:
            endpoint (str): Endpoint específico para la consulta.
            
        Returns:
            str: URL completa para la consulta a Guide to Pharmacology.
        """
        return f"{self.BASE_URL}/{endpoint}"
    
    def fetch(self, id: str) -> Dict[str, Any]:
        """
        Obtiene datos de Guide to Pharmacology para un símbolo de gen dado.
        
        Args:
            id (str): Símbolo del gen para la búsqueda
        
        Returns:
            Dict[str, Any]: Datos obtenidos de Guide to Pharmacology
        """
        # 1. Primero obtener el targetId a partir del símbolo
        url_targets = self._create_url_string("targets")
        targets_data = self._get_data(url_targets)
            
        target_id = None
        for target in targets_data:
            if target.get("abbreviation") == id:
                target_id = target.get("targetId")
                break
            
        if not target_id:
            return {
                "error": f"No se encontró el símbolo de gen '{id}' en Guide to Pharmacology."
            }
            
        # 2. Obtener los comentarios para el targetId
        url_comments = self._create_url_string(f"targets/{target_id}/comments")
        comments_data = self._get_data(url_comments)
            
        # 3. Obtener las interacciones y referencias para el targetId
        url_interactions = self._create_url_string(f"targets/{target_id}/interactions")
        interactions_data = self._get_data(url_interactions)
            
        # 4. Devolver todos los datos obtenidos
        return {
            "target_id": target_id,
            "comments": comments_data,
            "interactions": interactions_data
        }


    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos.
        """
        pass