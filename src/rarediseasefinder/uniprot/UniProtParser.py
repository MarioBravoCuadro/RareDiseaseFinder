import pandas as pd
from src.rarediseasefinder.core.constants import (
    QUICKGO_URL_TEMPLATE,
    PUBMED_URL_TEMPLATE,
    OMIM_URL_TEMPLATE,
    NOT_FOUND_MESSAGE
)

from ..core.parser import BaseParser

class UniProtParser(BaseParser):
    """Clase para transformar datos de UniProt en DataFrames estructurados"""
    
    @staticmethod
    def parse_function(data):
        """
        Extrae información de función de una proteína
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            DataFrame: Información de función estructurada
        """
        return pd.DataFrame([{
            "Function": txt.get("value", ""),
            "EvidenceCode": ev.get("evidenceCode", NOT_FOUND_MESSAGE),
            "QuickGO": QUICKGO_URL_TEMPLATE.format(ev['evidenceCode']) if ev.get("evidenceCode") else NOT_FOUND_MESSAGE,
            "Source": ev.get("source", NOT_FOUND_MESSAGE),
            "PublicationID": ev.get("id", NOT_FOUND_MESSAGE),
            "PubMed": PUBMED_URL_TEMPLATE.format(ev['id']) if ev.get("id") else NOT_FOUND_MESSAGE,
        } for comment in data.get("comments", []) if comment.get("commentType") == "FUNCTION"
          for txt in comment.get("texts", [])
          for ev in txt.get("evidences", [{}])
        ])
    
    @staticmethod
    def parse_subcellular_location(data):
        """
        Extrae información de localización subcelular
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            DataFrame: Información de localización estructurada
        """
        return pd.DataFrame([{
            "Value": loc.get("location", {}).get("value", ""),
            "ID": loc.get("location", {}).get("id", "")
        } for comment in data.get("comments", []) if comment.get("commentType") == "SUBCELLULAR LOCATION"
          for loc in comment.get("subcellularLocations", [])
        ])
    
    @staticmethod
    def parse_go_terms(data):
        """
        Extrae términos GO asociados
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            DataFrame: Términos GO estructurados
        """
        return pd.DataFrame([
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
        ])
    
    @staticmethod
    def parse_disease(data):
        """
        Extrae información de enfermedades asociadas
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            DataFrame: Información de enfermedades estructurada
        """
        return pd.DataFrame([{
            "Nombre": comment.get("disease", {}).get("diseaseId"),
            "Acronym": comment.get("disease", {}).get("acronym"),
            "Description": comment.get("disease", {}).get("description"),
            "OMIM": OMIM_URL_TEMPLATE.format(comment.get("disease", {}).get("diseaseCrossReference", {}).get("id")),
            "Publications": ", ".join(ev.get("id") for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id"))
        } for comment in data.get("comments", []) if comment.get("commentType") == "DISEASE"
        ])
    
    @staticmethod
    def parse_disease_publications(data):
        """
        Extrae publicaciones relacionadas con enfermedades
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            DataFrame: Publicaciones estructuradas
        """
        return pd.DataFrame([{
            "DiseaseID": comment.get("disease", {}).get("diseaseId"),
            "PubMed": PUBMED_URL_TEMPLATE.format(ev.get("id"))
        } for comment in data.get("comments", []) if comment.get("commentType") == "DISEASE"
          for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id")
        ])
    
    @staticmethod
    def parse_variants(data):
        """
        Extrae información de variantes naturales
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            DataFrame: Información de variantes estructurada
        """
        return pd.DataFrame({
            "Description": [feature.get("description")
                           for feature in data.get("features", [])
                           if feature.get("type") == "Natural variant"],
            "Publications": [", ".join(ev.get("id") for ev in feature.get("evidences", [])
                            if ev.get("id"))
                            for feature in data.get("features", [])
                            if feature.get("type") == "Natural variant"]
        })
    
    @staticmethod
    def parse_interactions(data):
        """
        Extrae información de interacciones proteína-proteína
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            DataFrame: Información de interacciones estructurada
        """
        return pd.DataFrame([{
            "Interactor": inter.get("interactantTwo", {}).get("uniProtKBAccession"),
            "GeneName": inter.get("interactantTwo", {}).get("geneName"),
            "NumExperiments": inter.get("numberOfExperiments")
        } for comment in data.get("comments", []) if comment.get("commentType") == "INTERACTION"
          for inter in comment.get("interactions", [])
        ]).sort_values(by="NumExperiments", ascending=False)
    
    @classmethod
    def parse_all(cls, data):
        """
        Procesa todos los tipos de datos disponibles
        
        Args:
            data (dict): Datos crudos de UniProt
            
        Returns:
            dict: Diccionario con todos los DataFrames procesados
        """
        if not data:
            return {}
            
        return {
            "Function": cls.parse_function(data),
            "Subcellular Location": cls.parse_subcellular_location(data),
            "GO Terms": cls.parse_go_terms(data),
            "Disease": cls.parse_disease(data),
            "Disease Publications": cls.parse_disease_publications(data),
            "Variants": cls.parse_variants(data),
            "Interactions": cls.parse_interactions(data)
        }


# uniprot/errors.py
class UniProtError(Exception):
    """Excepción base para errores relacionados con UniProt"""
    pass

class UniProtHTTPError(UniProtError):
    """Error de comunicación con la API de UniProt"""
    pass

class UniProtParsingError(UniProtError):
    """Error al procesar datos de UniProt"""
    pass