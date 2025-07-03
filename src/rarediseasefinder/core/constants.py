# URLs base
UNIPROT_BASE_URL = "https://rest.uniprot.org/uniprotkb"
PHAROS_BASE_URL = "https://pharos-api.ncats.io/graphql"
SELLECKCHEM_BASE_URL = "https://www.selleckchem.com"
DRUG_CENTRAL_BASE_URL = "https://drugcentral.org{}"

# Plantillas de URL
QUICKGO_URL_TEMPLATE = "https://www.ebi.ac.uk/QuickGO/term/{}"
PUBMED_URL_TEMPLATE = "https://pubmed.ncbi.nlm.nih.gov/{}"
OMIM_URL_TEMPLATE = "https://www.omim.org/entry/{}"
PHAROS_URL_TEMPLATE = "https://pharos.nih.gov/targets/{}"
REACTOME_URL_TEMPLATE = "https://reactome.org/content/detail/{}"
PUBCHEM_REACTOME_URL_TEMPLATE = "https://pubchem.ncbi.nlm.nih.gov/pathway/Reactome:{}"
CHEMBL_URL_TEMPLATE = "https://www.ebi.ac.uk/chembl/explore/compound/{}#DrugIndications"
UNIPROT_URL_TEMPLATE = "https://www.uniprot.org/uniprotkb/{}/entry"

# Enlaces externos nuevos
PATHWAYCOMMONS_URL_TEMPLATE = "https://apps.pathwaycommons.org/search?type=Pathway&q={}"
MALACARDS_URL_TEMPLATE = "https://www.malacards.org/search/results?q={}"
STRINGDB_URL_TEMPLATE = "https://string-db.org/network/9606.{}"  # Requiere Ensembl ID
INTACT_UNIPROT_URL_TEMPLATE = "https://www.uniprot.org/uniprotkb/{}/publications?facets=categories%3AInteraction"
INTACT_EBI_URL_TEMPLATE = "https://www.ebi.ac.uk/intact/search?query={}&interactionTypesFilter=direct%20interaction"
FUNCTIONOME_URL_TEMPLATE = "https://functionome.geneontology.org/gene/UniProtKB:{}"
ALPHAFOLD_URL_TEMPLATE = "https://alphafold.ebi.ac.uk/entry/{}"
ORPHANET_URL_TEMPLATE = "https://www.orpha.net/es/disease/gene/{}"
PHARMGKB_SEARCH_URL_TEMPLATE = "https://www.pharmgkb.org/search?query={}"

# URLs específicas de parsers
GUIDETOPHARMACOLOGY_TARGET_URL_TEMPLATE = "https://www.guidetopharmacology.org/GRAC/ObjectDisplayForward?objectId={}"
GUIDETOPHARMACOLOGY_LIGAND_URL_TEMPLATE = "https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId={}"
PANTHER_GO_URL_TEMPLATE = "http://www.pantherdb.org/panther/category.do?categoryAcc={}"
DRUGCENTRAL_SEARCH_URL_TEMPLATE = "https://drugcentral.org/drugcard/{}"
PANTHER_PATHWAY_URL_TEMPLATE = "https://pantherdb.org/pathway/pathwayDiagram.jsp?catAccession={}"

# Mensajes
NOT_FOUND_MESSAGE = "⚠️ No se han encontrado datos."
NO_DATA_MARKER = "NO DATA"

def get_standard_external_links(search_term: str) -> list:
    """
    Genera la lista estándar de enlaces externos para cualquier término de búsqueda.
    
    Args:
        search_term (str): Término de búsqueda
        
    Returns:
        list: Lista de diccionarios con enlaces externos
    """
    return [
        {
            "Nombre": "PathwayCommons",
            "Enlace": PATHWAYCOMMONS_URL_TEMPLATE.format(search_term),
            "Descripción": "Base de datos de vías de señalización biológicas",
        },
        {
            "Nombre": "MalaCards",
            "Enlace": MALACARDS_URL_TEMPLATE.format(search_term),
            "Descripción": "Base de datos de enfermedades humanas",
        },
        {
            "Nombre": "Orphanet",
            "Enlace": ORPHANET_URL_TEMPLATE.format(search_term),
            "Descripción": "Portal de enfermedades raras y medicamentos huérfanos",
        },
        {
            "Nombre": "PharmGKB",
            "Enlace": PHARMGKB_SEARCH_URL_TEMPLATE.format(search_term),
            "Descripción": "Base de datos de farmacogenómica (búsqueda general)"
        }
    ]

def get_uniprot_external_links(uniprot_id: str) -> list:
    """
    Genera enlaces externos específicos de UniProt.
    
    Args:
        uniprot_id (str): ID de UniProt
        
    Returns:
        list: Lista de diccionarios con enlaces externos de UniProt
    """
    if not uniprot_id:
        return []
    
    return [
        {
            "Nombre": "IntAct (UniProt)",
            "Enlace": INTACT_UNIPROT_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Base de datos de interacciones moleculares - UniProt",
        },
        {
            "Nombre": "IntAct (EBI)",
            "Enlace": INTACT_EBI_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Base de datos de interacciones moleculares - EBI",
        },
        {
            "Nombre": "FunctiOnome",
            "Enlace": FUNCTIONOME_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Análisis funcional basado en Gene Ontology",
        },
        {
            "Nombre": "AlphaFold",
            "Enlace": ALPHAFOLD_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Base de datos de estructuras proteicas predichas por IA",
        }
    ]