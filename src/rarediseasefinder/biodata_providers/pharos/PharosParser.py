from typing import Dict, List, Any

import pandas as pd

from ...core.BaseParser import BaseParser
from ...core.constants import NOT_FOUND_MESSAGE


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
            list: Lista de relaciones ordenadas por prioridad de clase (limitada a 10).
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

    def _decode_protein_to_protein_filters(self, filters: list) -> Dict[str, Dict]:
        """
        Devuelve los filtros de prioridad para el procesador 'Pharos'.
        
        Args:
            filters (list): Lista de diccionarios de filtros.
            
        Returns:
            Dict[str, Dict]: Diccionario con prioridades de clases y propiedades.
                            En caso de no encontrarse, devuelve un diccionario vacío.
        """
        for processor in filters:
            if processor["procesador"] == "Pharos":
                prioridad_clases = processor["prioridad_clases"]
                prioridad_propiedades = processor["prioridad_propiedades"]
                filtros = {
                    "prioridad_clases": prioridad_clases,
                    "prioridad_propiedades": prioridad_propiedades
                }
                return filtros
        # En caso de no encontrarse, devuelve un diccionario vacío.
        return {"prioridad_clases": {}, "prioridad_propiedades": {}}

    def _get_protein_to_protein_ordered(self, data: dict, filtros: list) -> List[Dict[str, Any]]:
        """
        Genera una lista de relaciones proteína-proteína priorizadas según las clases y propiedades indicadas.
        
        Args:
            data (dict): Diccionario con los datos del target.
            filtros (list): Lista de filtros que contienen las prioridades.
            
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con las relaciones proteína-proteína priorizadas.
        """
        filtros_decodificados = self._decode_protein_to_protein_filters(filtros)
        prioridad_clases = filtros_decodificados.get("prioridad_clases")
        prioridad_propiedades = filtros_decodificados.get("prioridad_propiedades")

        relaciones = []
        relaciones_raw = data.get("relacionProteinaProteina", [])
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

    def create_info_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con la información principal del target.
        
        Args:
            data (dict): Diccionario con los datos del target.
            
        Returns:
            pd.DataFrame: DataFrame con la información principal.
        """
        info_data = [NOT_FOUND_MESSAGE]
        if data:
          info_data = [{key: data[key] for key in ["nombre", "uniprot_ID", "descripcion", "claseDiana", "secuencia"]}]
        return self.parse_to_dataframe(info_data)

    def create_omim_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con las referencias OMIM.
        
        Args:
            data (dict): Diccionario con los datos del target.
            
        Returns:
            pd.DataFrame: DataFrame con las referencias OMIM.
        """
        omim_data = [NOT_FOUND_MESSAGE]
        if data:
          omim_data = data.get("referenciaOMIM", [])
        return self.parse_to_dataframe(omim_data)

    def create_protein_protein_relations_df(self, data: dict, filter_params: Dict[str, Any]) -> pd.DataFrame:
        """
        Crea un DataFrame con las relaciones proteína-proteína priorizadas.
        
        Args:
            data (dict): Diccionario con los datos del target.
            filter_params (Dict[str, Any]): Parámetros de filtrado que incluyen prioridades de clases y propiedades.
            
        Returns:
            pd.DataFrame: DataFrame con las relaciones proteína-proteína priorizadas.
        """
        relations_data = [NOT_FOUND_MESSAGE]
        if data:
            prioridad_clases = filter_params.get("PRIORIDAD_CLASES", {})
            prioridad_propiedades = filter_params.get("PRIORIDAD_PROPIEDADES", {})
            relations_data = self._get_protein_to_protein_ordered(data, [{
                "procesador": "Pharos",
                "prioridad_clases": prioridad_clases,
                "prioridad_propiedades": prioridad_propiedades
            }])
        return self.parse_to_dataframe(relations_data)

    def create_numero_vias_por_fuente_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con el número de vías por fuente.
        
        Args:
            data (dict): Diccionario con los datos del target.
            
        Returns:
            pd.DataFrame: DataFrame con el número de vías por fuente.
        """
        vias_data = [NOT_FOUND_MESSAGE]
        if data:
             vias_data = data.get("numeroDeViasPorFuente", [])
        return self.parse_to_dataframe(vias_data)

    def create_vias_df(self, data: dict) -> pd.DataFrame:
        """
        Crea un DataFrame con las vías.
        
        Args:
            data (dict): Diccionario con los datos del target.
            
        Returns:
            pd.DataFrame: DataFrame con las vías.
        """
        vias_data = [NOT_FOUND_MESSAGE]
        if data:
         vias_data = data.get("vias", [])
        return self.parse_to_dataframe(vias_data)

