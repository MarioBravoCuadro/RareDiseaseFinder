from unipressed import *
import pandas as pd
from IPython.display import display, Markdown
def mostrar_dataframe(titulo, df):
      """ Muestra un DataFrame con título o un mensaje si está vacío """
      display(Markdown(f"## {titulo}"))
      if df.empty:
          display(Markdown("> ⚠️ No se han encontrado datos."))
      else:
          display(Markdown(df.to_markdown(index=False)))

def procesar_uniprot(uniProtID):
    data = UniprotkbClient.fetch_one(uniProtID, parse=True)

    # 1. Función
    df_function = pd.DataFrame([{
        "Function": txt.get("value", ""),
        "EvidenceCode": ev.get("evidenceCode", "⚠️ No se han encontrado datos."),
        "QuickGO": f"https://www.ebi.ac.uk/QuickGO/term/{ev['evidenceCode']}" if ev.get("evidenceCode") else "⚠️ No se han encontrado datos.",
        "Source": ev.get("source","⚠️ No se han encontrado datos."),
        "PublicationID": ev.get("id","⚠️ No se han encontrado datos."),
        "PubMed": f"https://pubmed.ncbi.nlm.nih.gov/{ev['id']}" if ev.get("id") else "⚠️ No se han encontrado datos.",

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
    "OMIM": f"https://www.omim.org/entry/"+comment.get("disease", {}).get("diseaseCrossReference", {}).get("id"),
    "Publications": ", ".join(ev.get("id") for ev in comment.get("disease", {}).get("evidences", []) if ev.get("id"))
    } for comment in data.get("comments", []) if comment.get("commentType") == "DISEASE"
    ])

    df_disease_publications = pd.DataFrame([{
    "DiseaseID": comment.get("disease", {}).get("diseaseId"),  # Clave foránea
    "PubMed": f"https://pubmed.ncbi.nlm.nih.gov/"+ev.get("id")
    } for comment in data.get("comments", []) if comment.get("commentType") == "DISEASE"
    for ev in comment.get("disease", {}).get("evidences", [])])

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
    
    return {
        "Function": df_function,
        "Subcellular Location": df_subcellular,
        "Disease": df_disease,
        "Variants": df_variants,
        "Interactions": df_interactions
    }

   