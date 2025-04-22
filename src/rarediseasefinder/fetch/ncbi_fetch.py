import requests
import xml.etree.ElementTree as ET
import time
import pandas as pd

def obtener_abstract_pubmed(pubmed_id):
    """Obtiene el abstract de un artículo de PubMed dado su ID"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            abstract_element = root.find('.//AbstractText')
            
            if abstract_element is not None and abstract_element.text:
                return abstract_element.text
            return None
        else:
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def obtener_abstracts_batch(pubmed_ids, max_por_solicitud=100):
    """Obtiene los abstracts de múltiples artículos de PubMed"""
    resultados = {}
    
    for i in range(0, len(pubmed_ids), max_por_solicitud):
        lote_ids = pubmed_ids[i:i + max_por_solicitud]
        id_string = ",".join(lote_ids)
        
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id_string}&retmode=xml"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                articulos = root.findall('.//PubmedArticle')
                
                for articulo in articulos:
                    pmid_element = articulo.find('.//PMID')
                    if pmid_element is not None:
                        pmid = pmid_element.text
                        
                        abstract_element = articulo.find('.//AbstractText')
                        if abstract_element is not None and abstract_element.text:
                            resultados[pmid] = abstract_element.text
            
            time.sleep(0.4)  # Pausa para respetar los límites de la API
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    return resultados


def crear_dataframe_abstracts(df, columna_nombre='Nombre', columna_pubmed_id='Publications'):
    """
    Crea un nuevo DataFrame con nombre de enfermedad, link de publicación y abstract
    
    Args:
        df: DataFrame de entrada con enfermedades y publicaciones
        columna_nombre: Nombre de la columna que contiene el nombre de la enfermedad
        columna_pubmed_id: Nombre de la columna que contiene las publicaciones
        
    Returns:
        DataFrame con columnas: NombreEnfermedad, LinkPublicacion, Abstract
    """
    # Extraer todos los IDs de PubMed
    all_ids = []
    for pubmed_ids in df[columna_pubmed_id].dropna():
        ids = [pid.strip() for pid in str(pubmed_ids).split(', ') if pid.strip() and pid != 'Ref.91']
        all_ids.extend(ids)
    
    # Eliminar duplicados
    unique_ids = list(set(all_ids))
    
    # Obtener abstracts en lote
    abstracts_dict = obtener_abstracts_batch(unique_ids)
    
    # Crear los datos para el nuevo DataFrame
    resultados = []
    
    for _, row in df.iterrows():
        if pd.notna(row[columna_pubmed_id]):
            nombre_enfermedad = row[columna_nombre]
            # Obtener la lista de publicaciones
            ids = [pid.strip() for pid in str(row[columna_pubmed_id]).split(', ') if pid.strip() and pid != 'Ref.91']
            
            for pmid in ids:
                link_publicacion = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                abstract = abstracts_dict.get(pmid, "Abstract no disponible")
                
                resultados.append({
                    'NombreEnfermedad': nombre_enfermedad,
                    'LinkPublicacion': link_publicacion,
                    'Abstract': abstract
                })
    
    # Crear y devolver el nuevo DataFrame
    return pd.DataFrame(resultados)


__all__ = [
    'obtener_abstract_pubmed',
    'obtener_abstracts_batch',
    'crear_dataframe_abstracts'
]