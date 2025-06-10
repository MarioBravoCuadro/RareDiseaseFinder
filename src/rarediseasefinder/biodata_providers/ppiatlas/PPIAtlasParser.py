import pandas as pd
import numpy as np
from typing import Dict, Any

from ...core.BaseParser import BaseParser
from ...core.constants import NOT_FOUND_MESSAGE


class PPIAtlasParser(BaseParser):
    """
    Parser para datos de PPIAtlas.
    Transforma datos de interacciones proteína-proteína en DataFrames estructurados.
    """
    
    # Lista de tejidos/fuentes que pueden aparecer en PPIAtlas
    TISSUE_COLUMNS = [
        "blood", "brain", "breast", "colon", "kidney", 
        "liver", "lung", "ovary", "pancreas", 
        "stomach", "throat", "bioplex", "intact_humap"
    ]
    
    def __init__(self):
        """
        Inicializa el parser de PPIAtlas.
        """
        super().__init__()
    
    def parse_ppi_table(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Procesa los datos y crea una tabla con las interacciones proteína-proteína.
        Filtra por score >= 0.8 y reemplaza valores None/NaN por "-".
        
        Args:
            data (Dict[str, Any]): Datos pre-procesados del cliente.
            
        Returns:
            pd.DataFrame: Tabla de interacciones con el formato requerido.
        """
        # Caso de error
        if "error" in data:
            error_dict = {
                "protein": NOT_FOUND_MESSAGE,
                "avg_association_score": 0.0,
                "Error": data["error"]
            }
            for tissue in self.TISSUE_COLUMNS:
                error_dict[tissue] = "-"
            return self.parse_to_dataframe([error_dict])
        
        # Obtener registros y proteína consultada
        records = data.get("records", [])
        
        # Sin resultados
        if not records:
            empty_dict = {
                "protein": NOT_FOUND_MESSAGE,
                "avg_association_score": 0.0,
                "Error": "No interactions found"
            }
            for tissue in self.TISSUE_COLUMNS:
                empty_dict[tissue] = "-"
            return self.parse_to_dataframe([empty_dict])
        
        # Filtrar y transformar datos
        interactions = []
        for record in records:
            # Extraer y normalizar score (convertir None a 0)
            score = record.get("avg_association_score")
            if score is None:
                score = 0.0
                
            # Filtrar por score >= 0.8 (requerimiento de las investigadoras)
            if score >= 0.8:
                # Crear diccionario base con los campos principales
                interaction = {
                    "protein": record.get("protein2", NOT_FOUND_MESSAGE),
                    "avg_association_score": score
                }
                
                # Añadir todos los tejidos/fuentes, reemplazando None por "-"
                for tissue in self.TISSUE_COLUMNS:
                    tissue_score = record.get(tissue)
                    interaction[tissue] = tissue_score if tissue_score is not None else "-"
                
                interactions.append(interaction)
        
        # Sin interacciones con score >= 0.8
        if not interactions:
            no_interactions = {
                "protein": NOT_FOUND_MESSAGE,
                "avg_association_score": 0.0,
                "Error": "No interactions with score >= 0.8 found"
            }
            for tissue in self.TISSUE_COLUMNS:
                no_interactions[tissue] = "-"
            return self.parse_to_dataframe([no_interactions])
        
        # Ordenar por score descendente
        interactions.sort(key=lambda x: x["avg_association_score"], reverse=True)
        
        for interaction in interactions:
            # Asegurar que todas las columnas existan
            for tissue in self.TISSUE_COLUMNS:
                if tissue not in interaction:
                    interaction[tissue] = "-"
            
            # Reemplazar valores None/NaN por "-"
            for key, value in list(interaction.items()):
                if value is None or (isinstance(value, float) and np.isnan(value)):
                    interaction[key] = "-"
        
        # Convertir a DataFrame
        return self.parse_to_dataframe(interactions)