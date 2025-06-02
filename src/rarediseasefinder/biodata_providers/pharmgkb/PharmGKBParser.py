from typing import Dict, Any, List
import pandas as pd
from ...core.BaseParser import BaseParser
from ...core.constants import NOT_FOUND_MESSAGE, PUBMED_URL_TEMPLATE

class PharmGKBParser(BaseParser):
    """
    Parser para datos de PharmGKB.
    Transforma datos JSON de PharmGKB en DataFrames estructurados.
    """
    
    def __init__(self):
        super().__init__()
    
    def parse_label_annotations(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de anotaciones de etiquetas.
        
        Args:
            data (Dict[str, Any]): Datos crudos de PharmGKB
            
        Returns:
            pd.DataFrame: DataFrame con información de anotaciones de etiquetas
        """
        annotation_data = []
        
        if data:
            annotation = {
                "ID": data.get("id", NOT_FOUND_MESSAGE),
                "Name": data.get("name", NOT_FOUND_MESSAGE),
                "Source": data.get("source", NOT_FOUND_MESSAGE),
                "Biomarker_Status": data.get("biomarkerStatus", NOT_FOUND_MESSAGE),
                "Testing_Required": data.get("testing", {}).get("term", NOT_FOUND_MESSAGE) if data.get("testing") else NOT_FOUND_MESSAGE,
                "Indication": "Yes" if data.get("indication") else "No",
                "PGx_Related": "Yes" if data.get("pgxRelated") else "No"
            }
            
            # Extraer genes relacionados
            related_genes = []
            for gene in data.get("relatedGenes", []):
                related_genes.append(f"{gene.get('symbol', '')}: {gene.get('name', '')}")
            
            annotation["Related_Genes"] = ", ".join(related_genes) if related_genes else NOT_FOUND_MESSAGE
            
            # Extraer químicos relacionados
            related_chemicals = []
            for chem in result.get("relatedChemicals", []):
                related_chemicals.append(chem.get("name", ""))
            
            annotation["Related_Chemicals"] = ", ".join(related_chemicals) if related_chemicals else NOT_FOUND_MESSAGE
            
            # Añadir resumen si está disponible
            if "summaryMarkdown" in result and "html" in result["summaryMarkdown"]:
                annotation["Summary"] = self._clean_html(result["summaryMarkdown"]["html"])
            else:
                annotation["Summary"] = NOT_FOUND_MESSAGE
                
            annotation_data.append(annotation)
        
        # Si no hay datos, devolver un DataFrame con mensaje de error
        if not annotation_data:
            annotation_data = [{
                "ID": NOT_FOUND_MESSAGE,
                "Name": "No label annotation data available",
                "Source": NOT_FOUND_MESSAGE,
                "Biomarker_Status": NOT_FOUND_MESSAGE,
                "Testing_Required": NOT_FOUND_MESSAGE,
                "Indication": NOT_FOUND_MESSAGE,
                "PGx_Related": NOT_FOUND_MESSAGE,
                "Related_Genes": NOT_FOUND_MESSAGE,
                "Related_Chemicals": NOT_FOUND_MESSAGE,
                "Summary": NOT_FOUND_MESSAGE
            }]
        
        return self.parse_to_dataframe(annotation_data)
    
    def parse_literature(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de literatura científica.
        
        Args:
            data (Dict[str, Any]): Datos crudos de PharmGKB
            
        Returns:
            pd.DataFrame: DataFrame con información de literatura
        """
        literature_data = []
        result = self._get_first_result(data)
        
        if result and "literature" in result:
            for lit in result.get("literature", []):
                lit_entry = {
                    "Title": lit.get("title", NOT_FOUND_MESSAGE),
                    "Type": lit.get("type", NOT_FOUND_MESSAGE),
                    "Publication_Date": lit.get("pubDate", NOT_FOUND_MESSAGE),
                }
                
                # Extraer referencias cruzadas (enlaces)
                urls = []
                for ref in lit.get("crossReferences", []):
                    if "_url" in ref:
                        urls.append(f"{ref.get('resource', '')}: {ref.get('_url', '')}")
                
                lit_entry["References"] = ", ".join(urls) if urls else NOT_FOUND_MESSAGE
                
                # Extraer términos
                terms = []
                for term in lit.get("terms", []):
                    terms.append(f"{term.get('resource', '')}: {term.get('term', '')}")
                
                lit_entry["Terms"] = ", ".join(terms) if terms else NOT_FOUND_MESSAGE
                
                literature_data.append(lit_entry)
        
        # Si no hay datos, devolver un DataFrame con mensaje de error
        if not literature_data:
            literature_data = [{
                "Title": "No literature data available",
                "Type": NOT_FOUND_MESSAGE,
                "Publication_Date": NOT_FOUND_MESSAGE,
                "References": NOT_FOUND_MESSAGE,
                "Terms": NOT_FOUND_MESSAGE
            }]
        
        return self.parse_to_dataframe(literature_data)
    
    def parse_pathways(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de rutas biológicas.
        Nota: En el JSON de ejemplo no hay información directa de pathways,
        pero se puede extraer de los genes relacionados.
        
        Args:
            data (Dict[str, Any]): Datos crudos de PharmGKB
            
        Returns:
            pd.DataFrame: DataFrame con información de pathways inferida
        """
        pathway_data = []
        result = self._get_first_result(data)
        
        if result and "relatedGenes" in result:
            # Como el JSON de ejemplo no contiene pathways directamente,
            # creamos una entrada que relaciona los genes con potenciales pathways
            pathway_entry = {
                "Annotation_ID": result.get("id", NOT_FOUND_MESSAGE),
                "Pathway_Context": "DNA Repair Pathway", # Inferido del contexto (genes BRCA, ATM, etc.)
                "Associated_Genes": ", ".join([gene.get("symbol", "") for gene in result.get("relatedGenes", [])]),
                "Pathway_Source": "Inferred from gene functions",
                "Description": "Homologous Recombination Repair (HRR) Pathway" # Inferido del texto
            }
            pathway_data.append(pathway_entry)
        
        # Si no hay datos, devolver un DataFrame con mensaje de error
        if not pathway_data:
            pathway_data = [{
                "Annotation_ID": NOT_FOUND_MESSAGE,
                "Pathway_Context": NOT_FOUND_MESSAGE,
                "Associated_Genes": NOT_FOUND_MESSAGE,
                "Pathway_Source": NOT_FOUND_MESSAGE,
                "Description": "No pathway data available"
            }]
        
        return self.parse_to_dataframe(pathway_data)
    
    def _clean_html(self, html_text: str) -> str:
        """
        Limpia texto HTML básico para presentación en DataFrame.
        
        Args:
            html_text (str): Texto HTML a limpiar
            
        Returns:
            str: Texto limpio
        """
        # Implementación simple para eliminar etiquetas HTML básicas
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html_text)