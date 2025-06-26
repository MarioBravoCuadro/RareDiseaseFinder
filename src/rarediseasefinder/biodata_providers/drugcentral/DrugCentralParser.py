from typing import Dict, Any, List
import pandas as pd
from bs4 import BeautifulSoup

from ...core.BaseParser import BaseParser
from ...core.constants import NOT_FOUND_MESSAGE, NO_DATA_MARKER


class DrugCentralParser(BaseParser):
    """
    Parser para datos de DrugCentral.
    Transforma datos HTML en DataFrames estructurados.
    """
    
    def __init__(self):
        """
        Inicializa el parser de DrugCentral.
        """
        super().__init__()
    
    def parse_drug_results(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de medicamentos del HTML de DrugCentral.
        
        Args:
            data (Dict[str, Any]): Datos HTML de DrugCentral
            
        Returns:
            pd.DataFrame: DataFrame con información de medicamentos
        """
        if "error" in data:
            return self.parse_to_dataframe([
             {NO_DATA_MARKER: NOT_FOUND_MESSAGE}
            ])
            
        html = data.get("html", "")
        search_term = data.get("search_term", "")
        
        if not html:
            return self.parse_to_dataframe([{
                "DrugName": NOT_FOUND_MESSAGE,
                "Description": "No se encontraron datos HTML",
                "DrugID": NOT_FOUND_MESSAGE,
                "Link": NOT_FOUND_MESSAGE
            }])
            
        drugs_data = self._extract_drugs_from_html(html, search_term)
        
        if not drugs_data:
            return self.parse_to_dataframe([{
                "DrugName": NOT_FOUND_MESSAGE,
                "Description": "No se encontraron medicamentos relacionados",
                "DrugID": NOT_FOUND_MESSAGE,
                "Link": NOT_FOUND_MESSAGE
            }])
            
        return self.parse_to_dataframe(drugs_data)
    
    def _extract_drugs_from_html(self, html: str, search_term: str) -> List[Dict[str, str]]:
        """
        Extrae información de medicamentos del HTML de DrugCentral.
        
        Args:
            html (str): HTML de la página de resultados
            search_term (str): Término utilizado en la búsqueda
            
        Returns:
            List[Dict[str, str]]: Lista de medicamentos con sus datos
        """
        resultados = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Buscar la tabla de resultados
        tabla = soup.find('table')
        if not tabla:
            return []
        
        # Procesar cada fila de la tabla
        for fila in tabla.find_all('tr'):
            # Buscar las celdas de la fila
            celdas = fila.find_all('td')
            if len(celdas) < 2:
                continue
            
            # Extraer nombre y enlace
            primera_celda = celdas[0]
            enlace = primera_celda.find('a')
            if not enlace:
                continue
            
            # Obtener datos estructurados
            nombre = enlace.get_text().strip()
            href = enlace.get('href', '')
            link_completo = f"https://drugcentral.org{href}" if href else NOT_FOUND_MESSAGE
            
            # Obtener descripción
            descripcion = celdas[1].get_text().strip() if len(celdas) > 1 else NOT_FOUND_MESSAGE
            
            # Añadir a resultados
            resultados.append({
                "DrugName": nombre,
                "Description": descripcion,
                "Link": link_completo
            })
        
        return resultados