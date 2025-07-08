"""
Módulo para transformar datos de OpenTargets en DataFrames estructurados.
"""
from typing import Dict, Any

import pandas as pd
from rarediseasefinder.core.constants import REACTOME_URL_TEMPLATE, NO_DATA_MARKER, CHEMBL_URL_TEMPLATE

from ...core.BaseParser import BaseParser


class OpenTargetsParser(BaseParser):
    """
    Clase para transformar datos de OpenTargets en DataFrames estructurados.
    """
    def __init__(self):
        """
        Inicializa el parser de OpenTargets.
        """
        pass

    def create_basic_info_df(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información básica del target.
        
        Args:
            data (Dict[str, Any]): Datos crudos de OpenTargets.
            
        Returns:
            pd.DataFrame: Información básica estructurada.
        """
        info_data = [{
            "ID": data.get("id", ""),
            "Símbolo aprobado": data.get("approvedSymbol", ""),
            "Nombre aprobado": data.get("approvedName", "")
        }]
        return self.parse_to_dataframe(info_data)
    
    def create_pathways_df(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de vías biológicas.
        
        Args:
            data (Dict[str, Any]): Datos crudos de OpenTargets.
            
        Returns:
            pd.DataFrame: Información de vías estructurada.
        """
        pathways_data = []
        for pathway in data.get("pathways", []):
            pathways_data.append({
                "Link": REACTOME_URL_TEMPLATE.format(pathway.get("pathwayId", "")),
                "Vía": pathway.get("pathway", ""),
                "Término de nivel superior": pathway.get("topLevelTerm", "")
            })
        return self.parse_to_dataframe(pathways_data)
    
    def create_known_drugs_df(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de medicamentos conocidos.
        
        Args:
            data (Dict[str, Any]): Datos crudos de OpenTargets.
            
        Returns:
            pd.DataFrame: Información de medicamentos estructurada.
        """
        drugs_data = []
        if "knownDrugs" in data and "rows" in data["knownDrugs"]:
            for drug in data["knownDrugs"]["rows"]:
                drugs_data.append({
                    "CHEMBL Link": CHEMBL_URL_TEMPLATE.format(drug.get("drugId", "")),
                    "Nombre": drug.get("prefName", ""),
                    "Mecanismo de acción": drug.get("mechanismOfAction", ""),
                    "Fase": drug.get("phase", ""),
                    "Enfermedad": drug.get("disease", {}).get("name", "")
                })
        
        df = self.parse_to_dataframe(drugs_data)
        if not NO_DATA_MARKER in df.columns:
            # Ordenar por fase en orden descendente
            df = df.sort_values(by="Fase", ascending=False).drop_duplicates(subset=["CHEMBL Link"])
            df = df.reset_index(drop=True)
        return df
    
    def create_associated_diseases_df(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de enfermedades asociadas.
        
        Args:
            data (Dict[str, Any]): Datos crudos de OpenTargets.
            
        Returns:
            pd.DataFrame: Información de enfermedades estructurada.
        """
        diseases_data = []
        if "associatedDiseases" in data and "rows" in data["associatedDiseases"]:
            for disease in data["associatedDiseases"]["rows"]:
                diseases_data.append({
                    "Nombre": disease.get("disease", {}).get("name", ""),
                    "Descripción": disease.get("disease", {}).get("description", ""),
                    "Puntuación": round(disease.get("score", 0), 4)
                })
        
        return self.parse_to_dataframe(diseases_data)
    
    def create_interactions_df(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de interacciones proteína-proteína.
        
        Args:
            data (Dict[str, Any]): Datos crudos de OpenTargets.
            
        Returns:
            pd.DataFrame: Información de interacciones estructurada.
        """
        interactions_data = []
        if "interactions" in data and "rows" in data["interactions"]:
            for interaction in data["interactions"]["rows"]:
                interactor = interaction.get("intB")
                interactions_data.append({
                    "Proteína interactuante": interactor,
                    "Puntuación": interaction.get("score", 0)
                })
        
        df = self.parse_to_dataframe(interactions_data)
        if not NO_DATA_MARKER in df.columns:
            # Filtrar interacciones duplicadas o con el mismo target
            df = df[df["Proteína interactuante"] != data.get("approvedSymbol", "")]
            df = df.drop_duplicates(subset=["Proteína interactuante"])
            # Filtrar solo proteínas que empiecen por "ENSP"
            df = df[df["Proteína interactuante"].str.startswith("ENSP", na=False)]
        return df
    
    def create_mouse_phenotypes_df(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de fenotipos de ratón.
        
        Args:
            data (Dict[str, Any]): Datos crudos de OpenTargets.
            
        Returns:
            pd.DataFrame: Información de fenotipos estructurada.
        """
        phenotypes_data = []
        for phenotype in data.get("mousePhenotypes", []):
            literature_refs = []
            if phenotype.get("biologicalModels"):
                for model in phenotype["biologicalModels"]:
                    if model and "literature" in model:
                        
                        model_refs = model.get("literature", [])
                        if model_refs:
                            literature_refs.extend([ref for ref in model_refs if ref])
            
            phenotypes_data.append({
                "Fenotipo": phenotype.get("modelPhenotypeLabel", ""),
                "Referencias PubMed": ", ".join(set(literature_refs)) if literature_refs else "No disponible"
            })
        
        return self.parse_to_dataframe(phenotypes_data)