from typing import Dict, Any

import pandas as pd

from src.rarediseasefinder.core.constants import (
    QUICKGO_URL_TEMPLATE,
    PUBMED_URL_TEMPLATE,
    OMIM_URL_TEMPLATE,
    NOT_FOUND_MESSAGE
)
from ...core.BaseParser import BaseParser
"""Módulo para transformar datos de UniProt en DataFrames estructurados y proporcionar métodos de parseo."""

class UniProtParser(BaseParser):
    """Clase para transformar datos de UniProt en DataFrames estructurados"""
    
    def parse_function(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de función de una proteína
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt

        Returns:
            pd.DataFrame: Información de función estructurada con columnas para Función,
                         Código de evidencia, QuickGO, Fuente, ID de publicación y PubMed
        """
        function_data = [{
            "Function": txt.get("value", ""),
            "EvidenceCode": ev.get("evidenceCode", NOT_FOUND_MESSAGE),
            "QuickGO": QUICKGO_URL_TEMPLATE.format(ev['evidenceCode']) if ev.get("evidenceCode") else NOT_FOUND_MESSAGE,
            "Source": ev.get("source", NOT_FOUND_MESSAGE),
            "PublicationID": ev.get("id", NOT_FOUND_MESSAGE),
            "PubMed": PUBMED_URL_TEMPLATE.format(ev['id']) if ev.get("id") else NOT_FOUND_MESSAGE,
        } for comment in data.get("comments", []) if comment.get("commentType") == "FUNCTION"
          for txt in comment.get("texts", [])
          for ev in txt.get("evidences", [{}])
        ]
        return self.parse_to_dataframe(function_data)
    
    def parse_subcellular_location(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de localización subcelular
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Información de localización estructurada con valor e identificador
        """
        location_data = [{
            "Value": loc.get("location", {}).get("value", ""),
            "ID": loc.get("location", {}).get("id", "")
        } for comment in data.get("comments", []) if comment.get("commentType") == "SUBCELLULAR LOCATION"
          for loc in comment.get("subcellularLocations", [])
        ]
        return self.parse_to_dataframe(location_data)
    
    def parse_go_terms(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae términos GO (Gene Ontology) asociados
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Términos GO estructurados con ID, término, evidencia y enlace
        """
        go_terms_data = [
            {
                "GO_ID": reference.get("id", ""),
                "GO_TERM and Evidence": f"{go_term} ({evidence})" if go_term else "",
                "Link source": QUICKGO_URL_TEMPLATE.format(reference['id'])
            }
            for reference in data.get("uniProtKBCrossReferences", [])
            if reference.get("database") == "GO"
            for go_term, evidence in [(
                next((p["value"] for p in reference.get("properties", []) if p.get("key") == "GoTerm"), ""),
                next((p["value"] for p in reference.get("properties", []) if p.get("key") == "GoEvidenceType"), "")
            )]
        ]
        return self.parse_to_dataframe(go_terms_data)
    
    def parse_disease(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de enfermedades asociadas
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Información de enfermedades estructurada con nombre, acrónimo,
                         descripción, enlace OMIM y publicaciones relacionadas
        """
        disease_data = [{
            "Nombre": comment.get("disease", {}).get("diseaseId"),
            "Acronym": comment.get("disease", {}).get("acronym"),
            "Description": comment.get("disease", {}).get("description"),
            "OMIM": OMIM_URL_TEMPLATE.format(comment.get("disease", {}).get("diseaseCrossReference", {}).get("id")),
            "Publications": ", ".join(ev.get("id") for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id"))
        } for comment in data.get("comments", []) if comment.get("commentType") == "DISEASE"
        ]
        return self.parse_to_dataframe(disease_data)
    
    def parse_disease_publications(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae publicaciones relacionadas con enfermedades
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Publicaciones estructuradas con ID de enfermedad y enlace PubMed
        """
        publications_data = [{
            "DiseaseID": comment.get("disease", {}).get("diseaseId"),
            "PubMed": PUBMED_URL_TEMPLATE.format(ev.get("id"))
        } for comment in data.get("comments", []) if comment.get("commentType") == "DISEASE"
          for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id")
        ]
        return self.parse_to_dataframe(publications_data)
    
    def parse_variants(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de variantes naturales
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Información de variantes estructurada con descripción y publicaciones
        """
        variants_data = {
            "Description": [feature.get("description")
                           for feature in data.get("features", [])
                           if feature.get("type") == "Natural variant"],
            "Publications": [", ".join(ev.get("id") for ev in feature.get("evidences", [])
                            if ev.get("id"))
                            for feature in data.get("features", [])
                            if feature.get("type") == "Natural variant"]
        }
        return self.parse_to_dataframe(variants_data)
    
    def parse_interactions(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de interacciones proteína-proteína
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Información de interacciones estructurada con interactor,
                         nombre del gen y número de experimentos, ordenada por relevancia
        """
        interactions_data = [{
            "Interactor": inter.get("interactantTwo", {}).get("uniProtKBAccession"),
            "GeneName": inter.get("interactantTwo", {}).get("geneName"),
            "NumExperiments": inter.get("numberOfExperiments")
        } for comment in data.get("comments", []) if comment.get("commentType") == "INTERACTION"
          for inter in comment.get("interactions", [])
        ]
        # El ordenamiento se hace ahora dentro de parse_to_dataframe con un parámetro
        return self.parse_to_dataframe(interactions_data, sort_by="NumExperiments", ascending=False)