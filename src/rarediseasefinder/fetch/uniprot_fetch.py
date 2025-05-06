import pandas as pd
import requests
from .ncbi_fetch import crear_dataframe_abstracts

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    return None

def fetch_uniprot_data(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}"
    return fetch_data(url)

def procesar_uniprot(uniProtID):
    data = fetch_uniprot_data(uniProtID)

    # 1. Función
    df_function = pd.DataFrame([{
        "Function": txt.get("value", ""),
        "UniProtID": uniProtID,
        "QuickGO": f"https://www.ebi.ac.uk/QuickGO/term/{ev['evidenceCode']}" if ev.get("evidenceCode") else "⚠️ No se han encontrado datos.",
        "PubMed": f"https://pubmed.ncbi.nlm.nih.gov/{ev['id']}" if ev.get("id") else "⚠️ No se han encontrado datos.",
        "Alphafold": f"https://alphafold.ebi.ac.uk/entry/{uniProtID}",
        "Secuence": data.get("sequence", {}).get("value","⚠️ No se han encontrado datos."),   
    } for comment in data.get("comments", []) if comment.get("commentType") == "FUNCTION"
      for txt in comment.get("texts", [])
      for ev in txt.get("evidences", [{}])
      ])

    # 2. Subcellular Location (desnormalizado)

    df_subcellular = pd.DataFrame([{
        "Value": loc.get("location", {}).get("value", ""),
        "ID": loc.get("location", {}).get("id", "")
    }
    for comment in data.get("comments", []) if comment.get("commentType") == "SUBCELLULAR LOCATION"
    for loc in comment.get("subcellularLocations", [])
    ])

    df_subcellular_godata = pd.DataFrame([
        {
            "GO_ID": reference.get("id", ""),
            "GO_TERM and Evidence": f"{go_term} ({evidence})" if go_term else "",
            "Link source": f"https://www.ebi.ac.uk/QuickGO/term/{reference['id']}"
        }
        for reference in data.get("uniProtKBCrossReferences", [])
        if reference.get("database") == "GO"
        for go_term, evidence in [(
            next((p["value"] for p in reference.get("properties", []) if p.get("key") == "GoTerm"), ""),
            next((p["value"] for p in reference.get("properties", []) if p.get("key") == "GoEvidenceType"), "")
        )]
    ])


    # 3. Enfermedades (desnormalizado)
    df_disease = pd.DataFrame([{

    "Nombre": comment.get("disease", {}).get("diseaseId"),
    "Acronym": comment.get("disease", {}).get("acronym"),
    "Description": comment.get("disease", {}).get("description"),
    "OMIM": f"https://www.omim.org/entry/{comment.get('disease', {}).get('diseaseCrossReference', {}).get('id')}" if comment.get('disease', {}).get('diseaseCrossReference', {}).get('id') else "⚠️ No se han encontrado datos.",
    "Publications": ", ".join(ev.get("id") for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id"))
    } for comment in data.get("comments", []) if comment.get("commentType") == "DISEASE"
    ])

    # 4. Variantes (desnormalizado)
    df_variants = pd.DataFrame({
        "Description": [feature.get("description")
                        for feature in data.get("features", [])
                        if feature.get("type") == "Natural variant"],
        "Publications": [", ".join(ev.get("id") for ev in feature.get("evidences", [])
                         if ev.get("id"))
                         for feature in data.get("features", [])
                         if feature.get("type") == "Natural variant"]
    })

    # 5. Interacciones (desnormalizado)
    df_interactions = pd.DataFrame([{
        "Interactor": inter.get("interactantTwo", {}).get("uniProtKBAccession"),
        "GeneName": inter.get("interactantTwo", {}).get("geneName"),
        "NumExperiments": inter.get("numberOfExperiments")
    } for comment in data.get("comments", []) if comment.get("commentType") == "INTERACTION"
      for inter in comment.get("interactions", [])

    ]).sort_values(by="NumExperiments", ascending=False)
    
    # 6. Publicaciones con abstracts
    df_publicaciones = crear_dataframe_abstracts(df_disease)

    return {
        "Function": df_function,
        "Subcellular Location": df_subcellular,
        "Disease": df_disease,
        "Variants": df_variants,
        "Interactions": df_interactions,
        "Publicaciones": df_publicaciones 
    }

def procesar_uniprot_target(target):
    url = f"https://rest.uniprot.org/uniprotkb/search?query=gene:{target}+AND+reviewed:true&format=json"
    data = fetch_data(url)
    uniProtID = data["results"][0]["primaryAccession"]
    return procesar_uniprot(uniProtID)


__all__ = ['procesar_uniprot','procesar_uniprot_target']

   