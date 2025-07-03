import pandas as pd
from typing import Dict, Any

from ...core.BaseParser import BaseParser
from ...core.constants import (NOT_FOUND_MESSAGE, 
                               PANTHER_GO_URL_TEMPLATE, 
                               PANTHER_PATHWAY_URL_TEMPLATE)


class PantherParser(BaseParser):
    """
    Parser para datos obtenidos de PantherDB.
    Esta clase implementa métodos para extraer y formatear información específica de los datos
    de PantherDB.
    """
    
    # Mapeo de tipos de contenido a etiquetas legibles
    CONTENT_TYPE_LABELS = {
        "ANNOT_TYPE_ID_PANTHER_GO_SLIM_MF": "PANTHER GO-slim Molecular Function",
        "ANNOT_TYPE_ID_PANTHER_GO_SLIM_BP": "PANTHER GO-slim Biological Process",
        "ANNOT_TYPE_ID_PANTHER_GO_SLIM_CC": "PANTHER GO-slim Cellular Component",
        "ANNOT_TYPE_ID_PANTHER_PC": "PANTHER protein class",
        "ANNOT_TYPE_ID_PANTHER_PATHWAY": "PANTHER pathway"
    }
    
    VALID_CONTENT_TYPES = set(CONTENT_TYPE_LABELS.keys())

    def __init__(self):
        """
        Inicializa una instancia del parser de PantherDB.
        """
        super().__init__()

    def get_annotation_name(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae el nombre de la anotación de los datos proporcionados por PantherDB.
        
        Args:
            data (Dict[str, Any]): Datos obtenidos de la API de PantherDB.
            
        Returns:
            pd.DataFrame: DataFrame con el nombre de la anotación.
        """
        try:
            # Obtener la lista de annotations
            annotations = data['search']['mapped_genes']['gene']['annotation_type_list']['annotation_data_type']
            # Verificar que hay al menos 2 elementos (índice 1)
            if len(annotations) > 1:
                # Obtener el nombre de la annotation en la posición 1
                annotation_name = [annotations[1]['annotation_list']['annotation']['name']]
                return self.parse_to_dataframe({annotation_name[0]: ""})
            else:
                return self.parse_to_dataframe({"No hay suficientes annotations": ""})
        except KeyError as e:
            return self.parse_to_dataframe({f"Error al acceder a la clave: {e}": ""})
        except Exception as e:
            return self.parse_to_dataframe({f"Error inesperado: {e}": ""})

    def parse_annotations(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae anotaciones del JSON de PANTHER con tipos legibles.

        Args:
            data (Dict[str, Any]): JSON crudo de PANTHER.

        Returns:
            pd.DataFrame: DataFrame con columnas: ID, Nombre y Tipo de Anotación.
        """
        try:
            annotations_data = data["search"]["mapped_genes"]["gene"]["annotation_type_list"]["annotation_data_type"]
        except KeyError:
            return self.parse_to_dataframe([{
                "Annotation_Name": NOT_FOUND_MESSAGE,
                "Annotation_Type": NOT_FOUND_MESSAGE,
                "Annotation_ID": NOT_FOUND_MESSAGE
            }])

        parsed_annotations = []

        for entry in annotations_data:
            content_type = entry.get("content")
            if content_type in self.VALID_CONTENT_TYPES:
                readable_type = self.CONTENT_TYPE_LABELS.get(content_type, content_type)
                annotations = entry.get("annotation_list", {}).get("annotation", [])
                if isinstance(annotations, dict):
                    annotations = [annotations]
                for ann in annotations:
                    parsed_annotations.append({
                        "Annotation_Type": readable_type,
                        "Annotation_Name": ann.get("name", "N/A"),
                        "Annotation_ID": PANTHER_GO_URL_TEMPLATE.format(ann.get("id", "N/A"))
                    })

        if not parsed_annotations:
            parsed_annotations = [{
                "Annotation_Name": NOT_FOUND_MESSAGE,
                "Annotation_Type": NOT_FOUND_MESSAGE,
                "Annotation_ID": NOT_FOUND_MESSAGE,
            }]

        return self.parse_to_dataframe(parsed_annotations)

    def parse_pathways(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae solo los pathways del JSON de PANTHER.

        Args:
            data (Dict[str, Any]): JSON crudo de PANTHER.

        Returns:
            pd.DataFrame: DataFrame con nombre y link del pathway.
        """
        try:
            annotations_data = data["search"]["mapped_genes"]["gene"]["annotation_type_list"]["annotation_data_type"]
        except KeyError:
            return self.parse_to_dataframe([{
                "Pathway": NOT_FOUND_MESSAGE, 
                "Link": NOT_FOUND_MESSAGE
            }])

        pathway_entries = []

        for entry in annotations_data:
            if entry.get("content") == "ANNOT_TYPE_ID_PANTHER_PATHWAY":
                annotations = entry.get("annotation_list", {}).get("annotation", [])
                if isinstance(annotations, dict):
                    annotations = [annotations]
                for ann in annotations:
                    pathway_entries.append({
                        "Pathway": ann.get("name", "N/A"),
                        "Link": PANTHER_PATHWAY_URL_TEMPLATE.format(ann.get("id", "N/A"))
                    })

        if not pathway_entries:
            pathway_entries = [{
                "Pathway": NOT_FOUND_MESSAGE, 
                "Link": NOT_FOUND_MESSAGE
            }]

        return self.parse_to_dataframe(pathway_entries)