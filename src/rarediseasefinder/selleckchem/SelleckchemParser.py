import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict

from ..core.parser import BaseParser

class SelleckchemParser(BaseParser):
    """
    Clase para parsear la información de medicamentos de Selleckchem.
    """

    def __init__(self):
        super().__init__()

    def extraer_medicamentos(self,html) -> pd.DataFrame:
        """
        Extrae información de medicamentos de un HTML dado.
        Args:
            html (str): HTML de la página web que contiene la información de los medicamentos.
        Returns:
            List[Dict]: Lista de diccionarios con la información de los medicamentos.
        """
        soup = BeautifulSoup(html, 'html.parser')
        medicamentos = []
        filas = soup.find_all('tr', attrs={'name': 'productList'})
        for fila in filas:
            td_catalogo = fila.find('td', class_='posRel')
            catalogo = td_catalogo.get_text(strip=True) if td_catalogo else "N/A"
            enlace = fila.find('a', class_='blue f15 bold')
            nombre_producto = enlace.get_text(strip=True) if enlace else "N/A"
            link = enlace.get("href") if enlace else "N/A"
            p_tags = fila.find_all('p')
            descripcion = p_tags[1].get_text(strip=True) if len(p_tags) > 1 else "No description"
            medicamentos.append({
                "Catalog No.": catalogo,
                "Product Name": nombre_producto,
                "Link": link,
                "Description": descripcion
            })
        medicamentos_df = self.parse_to_dataframe(medicamentos)
        return medicamentos_df