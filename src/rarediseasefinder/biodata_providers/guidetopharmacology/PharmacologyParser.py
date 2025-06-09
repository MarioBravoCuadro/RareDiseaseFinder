from typing import Dict, Any
import pandas as pd

from ...core.BaseParser import BaseParser
from ...core.constants import NOT_FOUND_MESSAGE


class PharmacologyParser(BaseParser):
    """
    Parser para datos de Guide to Pharmacology.
    Transforma datos JSON en DataFrames estructurados.
    """
    
    def __init__(self):
        """
        Inicializa el parser de Guide to Pharmacology.
        """
        super().__init__()
    
    def parse_target_id(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae el ID del target encontrado.
        
        Args:
            data (Dict[str, Any]): Datos crudos de Guide to Pharmacology
            
        Returns:
            pd.DataFrame: DataFrame con el ID del target
        """
        if "error" in data:
            return self.parse_to_dataframe([{
                "TargetID": NOT_FOUND_MESSAGE,
                "Message": data.get("error", "Error desconocido")
            }])
        
        target_id = data.get("target_id", NOT_FOUND_MESSAGE)
        
        return self.parse_to_dataframe([{
            "TargetID": target_id,
            "URL": f"https://www.guidetopharmacology.org/GRAC/ObjectDisplayForward?objectId={target_id}"
        }])
    
    def parse_comments(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae comentarios sobre el target.
        
        Args:
            data (Dict[str, Any]): Datos crudos de Guide to Pharmacology
            
        Returns:
            pd.DataFrame: DataFrame con comentarios generales y de expresión génica/patofisiología
        """
        if "error" in data:
            return self.parse_to_dataframe([{
                "GeneralComments": NOT_FOUND_MESSAGE,
                "GeneExpressionAndPathophysiologyComments": NOT_FOUND_MESSAGE
            }])
        
        comments_data = data.get("comments", {})
        
        comments = {
            "GeneralComments": comments_data.get("generalComments", "").strip(),
            "GeneExpressionAndPathophysiologyComments": comments_data.get("geneExpressionPathophysiologyComments", "").strip()
        }
        
        # Si no hay datos, usar valores por defecto
        if not comments["GeneralComments"] and not comments["GeneExpressionAndPathophysiologyComments"]:
            comments = {
                "GeneralComments": "⚠️ No se han encontrado comentarios generales.",
                "GeneExpressionAndPathophysiologyComments": "⚠️ No se han encontrado comentarios de expresión génica/patofisiología."
            }
        
        return self.parse_to_dataframe([comments])
    
    def parse_references(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae referencias bibliográficas asociadas a interacciones.
        
        Args:
            data (Dict[str, Any]): Datos crudos de Guide to Pharmacology
            
        Returns:
            pd.DataFrame: DataFrame con referencias bibliográficas
        """
        if "error" in data:
            return self.parse_to_dataframe([{
                "Link": NOT_FOUND_MESSAGE,
                "Fuente": NOT_FOUND_MESSAGE,
                "ArticleTitle": NOT_FOUND_MESSAGE,
                "Authors": NOT_FOUND_MESSAGE
            }])
        
        interactions = data.get("interactions", [])
        references = []
        
        for interaction in interactions:
            for ref in interaction.get("refs", []):
                pmid = ref.get("pmid")
                reference_info = {
                    "Link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}" if pmid else NOT_FOUND_MESSAGE,
                    "Fuente": ref.get("title", NOT_FOUND_MESSAGE),
                    "ArticleTitle": ref.get("articleTitle", NOT_FOUND_MESSAGE),
                    "Authors": ref.get("authors", NOT_FOUND_MESSAGE)
                }
                references.append(reference_info)
        
        # Si no hay datos, usar valores por defecto
        if not references:
            references = [{
                "Link": NOT_FOUND_MESSAGE,
                "Fuente": "⚠️ No se han encontrado referencias bibliográficas.",
                "ArticleTitle": NOT_FOUND_MESSAGE,
                "Authors": NOT_FOUND_MESSAGE
            }]
        
        return self.parse_to_dataframe(references)
    
    def parse_interactions(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información sobre interacciones del target con ligandos.
        
        Args:
            data (Dict[str, Any]): Datos crudos de Guide to Pharmacology
            
        Returns:
            pd.DataFrame: DataFrame con información de interacciones
        """
        if "error" in data:
            return self.parse_to_dataframe([{
                "LigandName": NOT_FOUND_MESSAGE,
                "LigandType": NOT_FOUND_MESSAGE,
                "ActionType": NOT_FOUND_MESSAGE,
                "Affinity": NOT_FOUND_MESSAGE
            }])
        
        interactions = data.get("interactions", [])
        interactions_data = []
        
        for interaction in interactions:
            ligand = interaction.get("ligand", {})
            interaction_info = {
                "LigandName": ligand.get("name", NOT_FOUND_MESSAGE),
                "LigandType": ligand.get("type", NOT_FOUND_MESSAGE),
                "ActionType": interaction.get("type", NOT_FOUND_MESSAGE),
                "Affinity": interaction.get("affinity", NOT_FOUND_MESSAGE),
                "AffinityParameter": interaction.get("parameterName", NOT_FOUND_MESSAGE),
                "EndogenousCompound": "Yes" if ligand.get("isEndogenous", False) else "No"
            }
            interactions_data.append(interaction_info)
        
        # Si no hay datos, usar valores por defecto
        if not interactions_data:
            interactions_data = [{
                "LigandName": NOT_FOUND_MESSAGE,
                "LigandType": NOT_FOUND_MESSAGE,
                "ActionType": NOT_FOUND_MESSAGE,
                "Affinity": NOT_FOUND_MESSAGE,
                "AffinityParameter": NOT_FOUND_MESSAGE,
                "EndogenousCompound": NOT_FOUND_MESSAGE
            }]
        
        return self.parse_to_dataframe(interactions_data)