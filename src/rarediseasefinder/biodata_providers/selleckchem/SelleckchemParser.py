"""
Módulo de parser para extraer información de medicamentos de la web de Selleckchem.
Proporciona métodos para obtener listas y enlaces de productos como DataFrames de pandas.
"""
from typing import List, Dict

import pandas as pd
from bs4 import BeautifulSoup

from ...core.BaseParser import BaseParser


class SelleckchemParser(BaseParser):
    """
    Clase para parsear la información de medicamentos de Selleckchem.
    """

    def __init__(self):
        super().__init__()

    def extraer_medicamentos(self, html: str) -> pd.DataFrame:
        """
        Extrae información de medicamentos de un HTML dado.

        Args:
            html (str): Contenido HTML de la página con la lista de medicamentos.
        Returns:
            pd.DataFrame: DataFrame con los datos de los medicamentos extraídos.
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

    def obtener_link_selleckchem(self, html: str) -> pd.DataFrame:
        """
        Obtiene el primer enlace de producto de la lista de medicamentos.

        Args:
            html (str): Contenido HTML de la página con la lista de medicamentos.
        Returns:
            pd.DataFrame: DataFrame con el primer enlace completo o vacío si no hay productos.
        """
        productos = self.extraer_medicamentos(html)
        if not productos.empty:
            primer_link = f"www.selleckchem.com{productos.loc[0]['Link']}"
            return self.parse_to_dataframe([primer_link])
        return self.parse_to_dataframe([])

    def obtener_links_selleckchem(self, html: str) -> pd.DataFrame:
        """
        Obtiene todos los enlaces de productos de la lista de medicamentos.

        Args:
            html (str): Contenido HTML de la página con la lista de medicamentos.
        Returns:
            pd.DataFrame: DataFrame con los enlaces completos de todos los productos.
        """
        productos = self.extraer_medicamentos(html)
        links = []
        rango = range(len(productos))
        for i in rango:
            links.append(f"www.selleckchem.com{productos.loc[i]['Link']}")

        links = self.parse_to_dataframe(links)
        return links