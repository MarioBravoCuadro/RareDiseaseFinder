from typing import Dict, Any

import pandas as pd

from src.rarediseasefinder.core.constants import (
    QUICKGO_URL_TEMPLATE,
    PUBMED_URL_TEMPLATE,
    OMIM_URL_TEMPLATE,
    PHAROS_URL_TEMPLATE,
    NOT_FOUND_MESSAGE
)
from ...core.BaseParser import BaseParser
"""Módulo para transformar datos de UniProt en DataFrames estructurados y proporcionar métodos de parseo."""

class UniProtParser(BaseParser):
    """Clase para transformar datos de UniProt en DataFrames estructurados"""
    
    def _get_first_result(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrae el primer resultado de los datos crudos de UniProt o devuelve
        los datos directamente si es una respuesta de UniProt ID.
        Este método es útil para manejar diferentes formatos de respuesta.
        Se utiliza para asegurar que el formato de los datos es consistente.
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            Dict[str, Any]: Los datos procesados para su análisis
        """
        if "results" in data:
            # Caso de respuesta de Symbol
            return data.get("results", [])[0] if data.get("results") and len(data.get("results", [])) > 0 else {}
            # Caso de respuesta de UniProt ID
        if any(key in data for key in ["entryType", "primaryAccession", "uniProtkbId", "proteinDescription"]):
            return data
        
        return {}
    
    def parse_function(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de función de una proteína
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt

        Returns:
            pd.DataFrame: Información de función estructurada
        """
        # Extraer el primer resultado
        result = self._get_first_result(data)
        
        print("Estructura del resultado:", result.keys() if isinstance(result, dict) else "No es un diccionario")
        
        # A partir de aquí, usar 'result' en lugar de 'data'
        function_data = [{
            "Function": txt.get("value", ""),
            "EvidenceCode": ev.get("evidenceCode", NOT_FOUND_MESSAGE),
            "QuickGO": QUICKGO_URL_TEMPLATE.format(ev.get("evidenceCode")) if ev.get("evidenceCode") else NOT_FOUND_MESSAGE,
            "Source": ev.get("source", NOT_FOUND_MESSAGE),
            "PublicationID": ev.get("id", NOT_FOUND_MESSAGE),
            "PubMed": PUBMED_URL_TEMPLATE.format(ev.get("id")) if ev.get("id") else NOT_FOUND_MESSAGE,
        } for comment in result.get("comments", []) if comment.get("commentType") == "FUNCTION"
        for txt in comment.get("texts", [])
        for ev in txt.get("evidences", [{}])
        ]
        
        # Si no hay datos, usar datos de prueba
        if not function_data:
            function_data = [{
                "Function": "Función no disponible",
                "EvidenceCode": NOT_FOUND_MESSAGE,
                "QuickGO": NOT_FOUND_MESSAGE,
                "Source": NOT_FOUND_MESSAGE,
                "PublicationID": NOT_FOUND_MESSAGE,
                "PubMed": NOT_FOUND_MESSAGE
            }]
        
        return self.parse_to_dataframe(function_data)
    
    def parse_subcellular_location(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de localización subcelular
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Información de localización estructurada con valor e identificador
        """
        # Extraer el primer resultado
        result = self._get_first_result(data)
        
        location_data = [{
            "Value": loc.get("location", {}).get("value", ""),
            "ID": loc.get("location", {}).get("id", "")
        } for comment in result.get("comments", []) if comment.get("commentType") == "SUBCELLULAR LOCATION"
          for loc in comment.get("subcellularLocations", [])
        ]
        
        # Si no hay datos, usar datos de prueba
        if not location_data:
            location_data = [{
                "Value": "Localización no disponible",
                "ID": NOT_FOUND_MESSAGE
            }]
            
        return self.parse_to_dataframe(location_data)
    
    def parse_go_terms(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae términos GO (Gene Ontology) asociados
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Términos GO estructurados con ID, término, evidencia y enlace
        """
        # Extraer el primer resultado
        result = self._get_first_result(data)
        
        go_terms_data = [
            {
                "GO_ID": reference.get("id", ""),
                "GO_TERM and Evidence": f"{go_term} ({evidence})" if go_term else "",
                "Link source": QUICKGO_URL_TEMPLATE.format(reference.get("id", "")) if reference.get("id") else NOT_FOUND_MESSAGE
            }
            for reference in result.get("uniProtKBCrossReferences", [])
            if reference.get("database") == "GO"
            for go_term, evidence in [(
                next((p.get("value", "") for p in reference.get("properties", []) if p.get("key") == "GoTerm"), ""),
                next((p.get("value", "") for p in reference.get("properties", []) if p.get("key") == "GoEvidenceType"), "")
            )]
        ]
        
        # Si no hay datos, usar datos de prueba
        if not go_terms_data:
            go_terms_data = [{
                "GO_ID": NOT_FOUND_MESSAGE,
                "GO_TERM and Evidence": "Términos GO no disponibles",
                "Link source": NOT_FOUND_MESSAGE
            }]
            
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
        # Extraer el primer resultado
        result = self._get_first_result(data)
        
        disease_data = [{
            "Nombre": comment.get("disease", {}).get("diseaseId", ""),
            "Acronym": comment.get("disease", {}).get("acronym", ""),
            "Description": comment.get("disease", {}).get("description", ""),
            "OMIM": OMIM_URL_TEMPLATE.format(comment.get("disease", {}).get("diseaseCrossReference", {}).get("id", ""))
                if comment.get("disease", {}).get("diseaseCrossReference", {}).get("id") else NOT_FOUND_MESSAGE,
            "Publications": ", ".join(ev.get("id", "") for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id"))
        } for comment in result.get("comments", []) if comment.get("commentType") == "DISEASE"
        ]
        
        # Si no hay datos, usar datos de prueba
        if not disease_data:
            disease_data = [{
                "Nombre": "Enfermedad no disponible",
                "Acronym": NOT_FOUND_MESSAGE,
                "Description": NOT_FOUND_MESSAGE,
                "OMIM": NOT_FOUND_MESSAGE,
                "Publications": NOT_FOUND_MESSAGE
            }]
            
        return self.parse_to_dataframe(disease_data)
    
    def parse_disease_publications(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae publicaciones relacionadas con enfermedades
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Publicaciones estructuradas con ID de enfermedad y enlace PubMed
        """
        # Extraer el primer resultado
        result = self._get_first_result(data)
        
        publications_data = [{
            "DiseaseID": comment.get("disease", {}).get("diseaseId", ""),
            "PubMed": PUBMED_URL_TEMPLATE.format(ev.get("id", "")) if ev.get("id") else NOT_FOUND_MESSAGE
        } for comment in result.get("comments", []) if comment.get("commentType") == "DISEASE"
          for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id")
        ]
        
        # Si no hay datos, usar datos de prueba
        if not publications_data:
            publications_data = [{
                "DiseaseID": NOT_FOUND_MESSAGE,
                "PubMed": NOT_FOUND_MESSAGE
            }]
            
        return self.parse_to_dataframe(publications_data)
    
    def parse_variants(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de variantes naturales
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Información de variantes estructurada con descripción y publicaciones
        """
        # Extraer el primer resultado
        result = self._get_first_result(data)
        
        variants_data = [{
            "Description": feature.get("description", ""),
            "Publications": ", ".join(ev.get("id", "") for ev in feature.get("evidences", []) if ev.get("id"))
        } for feature in result.get("features", []) if feature.get("type") == "Natural variant"
        ]
        
        # Si no hay datos, usar datos de prueba
        if not variants_data:
            variants_data = [{
                "Description": "Variantes no disponibles",
                "Publications": NOT_FOUND_MESSAGE
            }]
            
        return self.parse_to_dataframe(variants_data)
    
    def parse_omim_references(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae referencias a la base de datos OMIM (MIM)

        Args:
            data (Dict[str, Any]): Datos crudos de UniProt

        Returns:
            pd.DataFrame: Referencias OMIM estructuradas
        """
        mim_data = []
        result = self._get_first_result(data)

        # Buscar referencias a OMIM
        for reference in result.get("uniProtKBCrossReferences", []):
            if reference.get("database") == "MIM":
                ref_id = reference.get("id", "")
                # Buscar propiedades si existen
                properties_value = ""
                if reference.get("properties") and len(reference.get("properties", [])) > 0:
                    properties_value = reference.get("properties")[0].get("value", "")

                mim_data.append({
                    "MIM_ID": ref_id,
                    "Description": properties_value,
                    "Link": f"{OMIM_URL_TEMPLATE.format(ref_id)}" if ref_id else NOT_FOUND_MESSAGE
                })

        # Si no hay datos, usar datos por defecto
        if not mim_data:
            mim_data = [{
                "MIM_ID": NOT_FOUND_MESSAGE,
                "Description": "Referencias OMIM no disponibles",
                "Link": NOT_FOUND_MESSAGE
            }]

        return self.parse_to_dataframe(mim_data)
    
    def parse_pharos_references(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae referencias a la base de datos Pharos

        Args:
            data (Dict[str, Any]): Datos crudos de UniProt

        Returns:
            pd.DataFrame: Referencias Pharos estructuradas
        """
        pharos_data = []
        result = self._get_first_result(data)
        # Buscar referencias a Pharos
        for reference in result.get("uniProtKBCrossReferences", []):
            if reference.get("database") == "Pharos":
                ref_id = reference.get("id", "")
                # Buscar propiedades si existen
                properties_value = ""
                if reference.get("properties") and len(reference.get("properties", [])) > 0:
                    properties_value = reference.get("properties")[0].get("value", "")

                pharos_data.append({
                    "Uniprot_ID": ref_id,
                    "TargetClass": properties_value,
                    "Link": f"{PHAROS_URL_TEMPLATE.format(ref_id)}" if ref_id else NOT_FOUND_MESSAGE
                })

        # Si no hay datos, usar datos por defecto
        if not pharos_data:
            pharos_data = [{
                "Pharos_ID": NOT_FOUND_MESSAGE,
                "Description": "Referencias Pharos no disponibles",
                "Link": NOT_FOUND_MESSAGE
            }]

        return self.parse_to_dataframe(pharos_data)
    
    def parse_interactions(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de interacciones proteína-proteína
        
        Args:
            data (Dict[str, Any]): Datos crudos de UniProt
            
        Returns:
            pd.DataFrame: Información de interacciones estructurada con interactor,
                         nombre del gen y número de experimentos, ordenada por relevancia
        """
        # Extraer el primer resultado
        result = self._get_first_result(data)
        
        interactions_data = [{
            "Interactor": inter.get("interactantTwo", {}).get("uniProtKBAccession", ""),
            "GeneName": inter.get("interactantTwo", {}).get("geneName", ""),
            "NumExperiments": inter.get("numberOfExperiments", 0)
        } for comment in result.get("comments", []) if comment.get("commentType") == "INTERACTION"
          for inter in comment.get("interactions", [])
        ]
        
        # Si no hay datos, usar datos de prueba
        if not interactions_data:
            interactions_data = [{
                "Interactor": NOT_FOUND_MESSAGE,
                "GeneName": NOT_FOUND_MESSAGE,
                "NumExperiments": 0
            }]
        
        # El ordenamiento se hace ahora dentro de parse_to_dataframe con un parámetro
        return self.parse_to_dataframe(interactions_data, sort_by="NumExperiments", ascending=False)