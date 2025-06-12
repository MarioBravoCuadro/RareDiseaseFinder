from typing import Dict, Any

import pandas as pd
from bs4 import BeautifulSoup

from ...core.BaseParser import BaseParser


class SelleckchemParser(BaseParser):
    """
    Clase para parsear la información de medicamentos de Selleckchem.
    """
    
    BASE_URL = "https://www.selleckchem.com"

    def __init__(self):
        super().__init__()

    def extraer_medicamentos(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de medicamentos de un HTML dado.

        Args:
            data (Dict[str, Any]): Diccionario con la clave 'html' que contiene el contenido HTML.
        Returns:
            pd.DataFrame: DataFrame con los datos de los medicamentos extraídos.
        """
        html = data.get('html')
        soup = BeautifulSoup(html, 'html.parser')
        medicamentos = []
        filas = soup.find_all('tr', attrs={'name': 'productList'})
        for fila in filas:
            td_catalogo = fila.find('td', class_='posRel')
            catalogo = td_catalogo.get_text(strip=True) if td_catalogo else "N/A"
            enlace = fila.find('a', class_='blue bold f15')
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

    def obtener_link_selleckchem(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Obtiene el primer enlace de producto de la lista de medicamentos.

        Args:
            data (Dict[str, Any]): Diccionario con la clave 'html' que contiene el contenido HTML.
        Returns:
            pd.DataFrame: DataFrame con el primer enlace completo o vacío si no hay productos.
        """
        productos = self.extraer_medicamentos(data)
        if not productos.empty:
            primer_link = f"{self.BASE_URL}{productos.loc[0]['Link']}"
            return self.parse_to_dataframe([primer_link])
        return self.parse_to_dataframe([])

    def obtener_links_selleckchem(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Obtiene todos los enlaces de productos de la lista de medicamentos.

        Args:
            data (Dict[str, Any]): Diccionario con la clave 'html' que contiene el contenido HTML.
        Returns:
            pd.DataFrame: DataFrame con los enlaces completos de todos los productos.
        """
        productos = self.extraer_medicamentos(data)
        links = []
        if not productos.empty:
            rango = range(len(productos))
            for i in rango:
                link = productos.loc[i]['Link']
                if link and link != "N/A":
                    links.append(f"{self.BASE_URL}{link}")

        return self.parse_to_dataframe(links)