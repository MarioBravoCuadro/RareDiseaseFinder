import pandas as pd
from typing import Dict, Any
from ...core.BaseParser import BaseParser
from ...core.constants import NOT_FOUND_MESSAGE


class PharmGKBParser(BaseParser):
    """
    Parser para datos de PharmGKB.
    Transforma datos JSON de PharmGKB en DataFrames estructurados.
    """
    
    def __init__(self):
        """
        Inicializa el parser de PharmGKB.
        """
        super().__init__()
    
    def parse_gene_symbols(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae símbolos de genes relacionados sin duplicados.

        Args:
            data (Dict[str, Any]): Datos crudos de PharmGKB

        Returns:
            pd.DataFrame: DataFrame con símbolos de genes sin duplicados
        """
        related_genes_data = []
        seen_symbols = set()  # Conjunto para rastrear símbolos ya procesados

        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            for result in data["data"]:
                for gene in result.get("relatedGenes", []):
                    symbol = gene.get("symbol", NOT_FOUND_MESSAGE)
                    name = gene.get("name", NOT_FOUND_MESSAGE)

                    # Procesar solo si el símbolo no ha sido visto antes
                    if symbol != NOT_FOUND_MESSAGE and symbol not in seen_symbols:
                        seen_symbols.add(symbol)  # Añadir al conjunto de símbolos vistos
                        related_gene = {
                            "Gene_Symbol": symbol,
                            "Gene_Name": name
                        }
                        related_genes_data.append(related_gene)

        # Si no hay datos, devolver un DataFrame con mensaje de error
        if not related_genes_data:
            related_genes_data = [{
                "Gene_Symbol": NOT_FOUND_MESSAGE,
                "Gene_Name": "No gene data available"
            }]

        # Crear y ordenar el DataFrame por símbolo de gen
        df = self.parse_to_dataframe(related_genes_data)
        if "Gene_Symbol" in df.columns and NOT_FOUND_MESSAGE not in df["Gene_Symbol"].values:
            df = df.sort_values("Gene_Symbol")

        return df

    def parse_label_annotations(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de anotaciones de etiquetas del JSON de PharmGKB.
        
        Args:
            data (Dict[str, Any]): Datos crudos de PharmGKB
            
        Returns:
            pd.DataFrame: DataFrame con información de anotaciones de etiquetas
        """
        annotation_data = []

        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            for result in data["data"]:
                id = result.get("id", NOT_FOUND_MESSAGE)
                link = f"https://www.pharmgkb.org/labelAnnotation/{id}"

                # Obtener genes para asociarlos a rutas
                genes = [gene.get("symbol", "") for gene in result.get("relatedGenes", [])]
                gene_string = ", ".join(genes) if genes else NOT_FOUND_MESSAGE

                # Inicializar resumen con valor por defecto
                summary = NOT_FOUND_MESSAGE
                
                # Añadir resumen si está disponible
                if "summaryMarkdown" in result and "html" in result["summaryMarkdown"]:
                    summary = BaseParser.clean_html(result["summaryMarkdown"]["html"])

                annotation = {
                    "Link": link,
                    "Name": result.get("name", NOT_FOUND_MESSAGE),
                    "Source": result.get("source", NOT_FOUND_MESSAGE),
                    "Associated_Genes": gene_string,
                    "Summary": summary,
                    "Biomarker_Status": result.get("biomarkerStatus", NOT_FOUND_MESSAGE),
                    "Testing_Required": result.get("testing", {}).get("term", NOT_FOUND_MESSAGE) if result.get("testing") else NOT_FOUND_MESSAGE,
                    "Indication": "Yes" if result.get("indication") else "No",
                    "PGx_Related": "Yes" if result.get("pgxRelated") else "No"
                }

                # Añadir la anotación a la lista
                annotation_data.append(annotation)
                
        # Si no hay datos, devolver un DataFrame con mensaje de error
        if not annotation_data:
            annotation_data = [{
                "Link": NOT_FOUND_MESSAGE,
                "Name": "No label annotation data available",
                "Source": NOT_FOUND_MESSAGE,
                "Associated_Genes": NOT_FOUND_MESSAGE,
                "Summary": NOT_FOUND_MESSAGE,
                "Biomarker_Status": NOT_FOUND_MESSAGE,
                "Testing_Required": NOT_FOUND_MESSAGE,
                "Indication": NOT_FOUND_MESSAGE,
                "PGx_Related": NOT_FOUND_MESSAGE
            }]
        
        # Filtrar solo EMA o FDA como se solicita
        filtered_data = [annotation for annotation in annotation_data if annotation["Source"] in ["EMA", "FDA"]]
        
        # Si no hay datos después del filtrado, usar los datos originales
        if not filtered_data and annotation_data[0]["Name"] != "No label annotation data available":
            filtered_data = annotation_data
            
        return self.parse_to_dataframe(filtered_data)

    def parse_literature(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Extrae información de literatura científica.
        
        Args:
            data (Dict[str, Any]): Datos crudos de PharmGKB
            
        Returns:
            pd.DataFrame: DataFrame con información de literatura
        """
        literature_data = []

        if "data" in data and isinstance(data["data"], list):
            for result in data["data"]:
                if "literature" in result:
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
        Extrae información de rutas biológicas del JSON de PharmGKB.
        
        Args:
            data (Dict[str, Any]): Datos crudos de PharmGKB
            
        Returns:
            pd.DataFrame: DataFrame con información de rutas biológicas
        """
        pathway_data = []

        if "data" in data and isinstance(data["data"], list):
            for result in data["data"]:
                if "relatedGenes" in result and "textMarkdown" in result:
                    # Obtener genes para asociarlos a rutas
                    genes = [gene.get("symbol", "") for gene in result.get("relatedGenes", [])]
                    gene_string = ", ".join(genes) if genes else NOT_FOUND_MESSAGE

                    id = result.get("id", NOT_FOUND_MESSAGE)
                    link = f"https://www.pharmgkb.org/labelAnnotation/{id}"

                    # Crear entrada de pathway
                    pathway_entry = {
                        "Annotation_ID": link,
                        "Summary": NOT_FOUND_MESSAGE,  # Inicializar con un valor por defecto
                        "Associated_Genes": gene_string
                    }

                    # Añadir resumen si está disponible
                    if "summaryMarkdown" in result and "html" in result["summaryMarkdown"]:
                        pathway_entry["Summary"] = BaseParser.clean_html(result["summaryMarkdown"]["html"])

                    pathway_data.append(pathway_entry)

        # Si no hay datos, devolver un DataFrame con mensaje de error
        if not pathway_data:
            pathway_data = [{
                "Annotation_ID": NOT_FOUND_MESSAGE,
                "Summary": NOT_FOUND_MESSAGE,
                "Associated_Genes": NOT_FOUND_MESSAGE
            }]

        return self.parse_to_dataframe(pathway_data)