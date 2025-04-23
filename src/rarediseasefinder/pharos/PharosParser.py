from ..core.parser import BaseParser

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

    def get_protein_to_protein_ordered_df(self, target_data: dict, prioridad_clases: dict[str, int],
                                          prioridad_propiedades: dict[str, int]):
        """
        Genera una lista de relaciones proteína-proteína priorizadas según las clases y propiedades indicadas.
        Args:
            target_data (dict): Diccionario con los datos del target.
            prioridad_clases (dict): Prioridad de las clases de diana.
            prioridad_propiedades (dict): Prioridad de las propiedades de relación.
        Returns:
            list: Lista de diccionarios con las relaciones priorizadas.
        """
        # Crear DataFrame de relaciones proteína-proteína con priorización
        relaciones = []

        # Ordenar y filtrar las relaciones
        relaciones_raw = target_data.get("relacionProteinaProteina", [])

        # ordenar por clase
        relaciones_ordenadas = sorted(
            relaciones_raw,
            key=lambda rel: prioridad_clases.get(rel.get("target", {}).get("claseDiana", ""), 5)
        )[:10]

        # Procesar solo las top 10
        for rel in relaciones_ordenadas:
            if "target" in rel and "propiedadesRelacion" in rel:  # comprobar estrucutra de la respuesta del target
                # Filtrar propiedades por relevancia (p_wrong, p_ni, p_int, novelty)
                propiedades_filtradas = []
                for prop in rel["propiedadesRelacion"]:
                    if prop["name"] in ["p_wrong", "p_ni"]:
                        # if prop["name"] in ["p_wrong", "p_ni", "p_int", "novelty"] Para sacar los cuatro tipos
                        propiedades_filtradas.append(prop)

                # Ordenar por propiedad
                propiedades_ordenadas = sorted(
                    propiedades_filtradas,
                    key=lambda x: prioridad_propiedades.get(x["name"], 5)
                )

                # Agregar solo las propiedades ordenadas
                for prop in propiedades_ordenadas:
                    relaciones.append({
                        "Proteina": rel["target"]["nombre"],
                        "Proteina_ID": rel["target"]["proteina_ID"],
                        "Clase Diana": rel["target"]["claseDiana"],
                        "Propiedad": prop["name"],
                        "Valor": prop["value"]
                    })
        return relaciones

    def parse(self, data: dict, prioridad_clases: dict, prioridad_propiedades: dict) -> dict:
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

        # Crear DataFrame con información principal
        df_info = pd.DataFrame([{key: data[key] for key in ["nombre", "uniprot_ID", "descripcion", "claseDiana", "secuencia"]}])

        # Crear DataFrame de referencia OMIM
        df_omim = pd.DataFrame(data.get("referenciaOMIM", []))

        #Crear DataFrame de proteina-proteina-ordenados
        df_relaciones = pd.DataFrame(self.get_protein_to_protein_ordered_df(data,prioridad_clases,prioridad_propiedades))

        # Crear Dataframe de numeroDeViasPorFuente
        df_numero_vias_por_fuente = pd.DataFrame(data.get("numeroDeViasPorFuente", []))

        # Crear DataFrame de vías
        df_vias = pd.DataFrame(data.get("vias", []))

        dataframes = {
            "info" : df_info,
            "omim" : df_omim,
            "protein_protein_relations" : df_relaciones,
            "numero_vias_fuente" : df_numero_vias_por_fuente,
            "vias" : df_vias
        }
        return  dataframes
