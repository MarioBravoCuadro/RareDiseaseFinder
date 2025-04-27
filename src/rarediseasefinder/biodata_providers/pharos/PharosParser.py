from ...core.BaseParser import BaseParser
from typing import Union, Dict, List

import pandas as pd


class PharosParser(BaseParser):
    """
    Clase para parsear y procesar datos obtenidos de Pharos.
    Incluye métodos para priorizar relaciones proteína-proteína y generar DataFrames con la información relevante.
    """
    def __init__(self):
        """
        Inicializa el parser de Pharos.
        """
        pass

    def _filtrar_propiedades(self, propiedades: list, propiedades_validas: list) -> list:
        """
        Filtra las propiedades relevantes de una relación.
        Args:
            propiedades (list): Lista de propiedades de la relación.
            propiedades_validas (list): Lista de nombres de propiedades válidas.
        Returns:
            list: Lista de propiedades filtradas.
        """
        return [prop for prop in propiedades if prop["name"] in propiedades_validas]

    def _ordenar_relaciones_por_clase(self, relaciones: list, prioridad_clases: dict) -> list:
        """
        Ordena las relaciones por prioridad de clase.
        Args:
            relaciones (list): Lista de relaciones.
            prioridad_clases (dict): Diccionario de prioridad de clases.
        Returns:
            list: Lista de relaciones ordenadas por prioridad de clase.
        """
        return sorted(
            relaciones,
            key=lambda rel: prioridad_clases.get(rel.get("target", {}).get("claseDiana", ""), 5)
        )[:10]

    def _ordenar_propiedades(self, propiedades: list, prioridad_propiedades: dict) -> list:
        """
        Ordena las propiedades por prioridad.
        Args:
            propiedades (list): Lista de propiedades.
            prioridad_propiedades (dict): Diccionario de prioridad de propiedades.
        Returns:
            list: Lista de propiedades ordenadas por prioridad.
        """
        return sorted(
            propiedades,
            key=lambda x: prioridad_propiedades.get(x["name"], 5)
        )

    def get_protein_to_protein_ordered_df(self, target_data: dict, prioridad_clases: dict[str, int],
                                          prioridad_propiedades: dict[str, int]) -> list:
        """
        Genera una lista de relaciones proteína-proteína priorizadas según las clases y propiedades indicadas.
        Args:
            target_data (dict): Diccionario con los datos del target.
            prioridad_clases (dict): Prioridad de las clases de diana.
            prioridad_propiedades (dict): Prioridad de las propiedades de relación.
        Returns:
            list: Lista de diccionarios con las relaciones priorizadas.
        """
        relaciones = []
        relaciones_raw = target_data.get("relacionProteinaProteina", [])
        relaciones_ordenadas = self._ordenar_relaciones_por_clase(relaciones_raw, prioridad_clases)

        for rel in relaciones_ordenadas:
            if "target" in rel and "propiedadesRelacion" in rel:
                propiedades_filtradas = self._filtrar_propiedades(rel["propiedadesRelacion"], ["p_wrong", "p_ni"])
                propiedades_ordenadas = self._ordenar_propiedades(propiedades_filtradas, prioridad_propiedades)
                for prop in propiedades_ordenadas:
                    relaciones.append({
                        "Proteina": rel["target"]["nombre"],
                        "Proteina_ID": rel["target"]["proteina_ID"],
                        "Clase Diana": rel["target"]["claseDiana"],
                        "Propiedad": prop["name"],
                        "Valor": prop["value"]
                    })
        return relaciones

    def _create_info_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con la información principal del target.
        Args:
            data (dict): Diccionario con los datos del target.
        Returns:
            pd.DataFrame: DataFrame con la información principal.
        """
        info_data = [{key: data[key] for key in ["nombre", "uniprot_ID", "descripcion", "claseDiana", "secuencia"]}]
        return self.parse_to_dataframe(info_data)

    def _create_omim_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con las referencias OMIM.
        Args:
            data (dict): Diccionario con los datos del target.
        Returns:
            pd.DataFrame: DataFrame con las referencias OMIM.
        """
        omim_data = data.get("referenciaOMIM", [])
        return self.parse_to_dataframe(omim_data)

    def _create_protein_protein_relations_df(self, data: dict, prioridad_clases: dict, prioridad_propiedades: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con las relaciones proteína-proteína priorizadas.
        Args:
            data (dict): Diccionario con los datos del target.
            prioridad_clases (dict): Prioridad de las clases de diana.
            prioridad_propiedades (dict): Prioridad de las propiedades de relación.
        Returns:
            pd.DataFrame: DataFrame con las relaciones proteína-proteína priorizadas.
        """
        relations_data = self.get_protein_to_protein_ordered_df(data, prioridad_clases, prioridad_propiedades)
        return self.parse_to_dataframe(relations_data)

    def _create_numero_vias_por_fuente_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con el número de vías por fuente.
        Args:
            data (dict): Diccionario con los datos del target.
        Returns:
            pd.DataFrame: DataFrame con el número de vías por fuente.
        """
        vias_data = data.get("numeroDeViasPorFuente", [])
        return self.parse_to_dataframe(vias_data)

    def _create_vias_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con las vías.
        Args:
            data (dict): Diccionario con los datos del target.
        Returns:
            pd.DataFrame: DataFrame con las vías.
        """
        vias_data = data.get("vias", [])
        return self.parse_to_dataframe(vias_data)

    def parse(self, data: dict, prioridad_clases: dict, prioridad_propiedades: dict) -> dict[str, pd.DataFrame]:
        """
        Parsea los datos de Pharos y los organiza en varios DataFrames.
        Args:
            data (dict): Datos crudos obtenidos de Pharos.
            prioridad_clases (dict): Prioridad de las clases de diana.
            prioridad_propiedades (dict): Prioridad de las propiedades de relación.
        Returns:
            dict: Diccionario con los DataFrames generados (info, omim, protein_protein_relations, numero_vias_fuente, vias).
        """
        print(type(data))
        print(data.keys())

        df_info = self._create_info_df(data)
        df_omim = self._create_omim_df(data)
        df_relaciones = self._create_protein_protein_relations_df(data, prioridad_clases, prioridad_propiedades)
        df_numero_vias_por_fuente = self._create_numero_vias_por_fuente_df(data)
        df_vias = self._create_vias_df(data)

        dataframes = {
            "info": df_info,
            "omim": df_omim,
            "protein_protein_relations": df_relaciones,
            "numero_vias_fuente": df_numero_vias_por_fuente,
            "vias": df_vias
        }
        return dataframes
