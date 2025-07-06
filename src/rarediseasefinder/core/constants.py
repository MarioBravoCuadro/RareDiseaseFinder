# URLs base
UNIPROT_BASE_URL = "https://rest.uniprot.org/uniprotkb"
PHAROS_BASE_URL = "https://pharos-api.ncats.io/graphql"
SELLECKCHEM_BASE_URL = "https://www.selleckchem.com"
DRUG_CENTRAL_BASE_URL = "https://drugcentral.org{}"
STRINGDB_BASE_URL = "https://string-db.org/api/json/get_string_ids?identifiers={}&species=9606"
STRINGDB_PING_URL = "https://string-db.org/api/json/version"

# Plantillas de URL
QUICKGO_URL_TEMPLATE = "https://www.ebi.ac.uk/QuickGO/term/{}"
PUBMED_URL_TEMPLATE = "https://pubmed.ncbi.nlm.nih.gov/{}"
OMIM_URL_TEMPLATE = "https://www.omim.org/entry/{}"
PHAROS_URL_TEMPLATE = "https://pharos.nih.gov/targets/{}"
REACTOME_URL_TEMPLATE = "https://reactome.org/content/detail/{}"
PUBCHEM_REACTOME_URL_TEMPLATE = "https://pubchem.ncbi.nlm.nih.gov/pathway/Reactome:{}"
CHEMBL_URL_TEMPLATE = "https://www.ebi.ac.uk/chembl/explore/compound/{}#DrugIndications"
UNIPROT_URL_TEMPLATE = "https://www.uniprot.org/uniprotkb/{}/entry"
HAMAP_URL_TEMPLATE = "https://hamap.expasy.org/rule/{}"

# Enlaces externos nuevos
PATHWAYCOMMONS_URL_TEMPLATE = "https://apps.pathwaycommons.org/search?type=Pathway&q={}"
MALACARDS_URL_TEMPLATE = "https://www.malacards.org/search/results?q={}"
STRINGDB_URL_TEMPLATE = "https://string-db.org/network/9606.{}"  # Requiere Ensembl ID
UNIPROT_INTERACTIONS_URL_TEMPLATE = "https://www.uniprot.org/uniprotkb/{}/publications?facets=categories%3AInteraction"
INTACT_EBI_URL_TEMPLATE = "https://www.ebi.ac.uk/intact/search?query={}"
FUNCTIONOME_URL_TEMPLATE = "https://functionome.geneontology.org/gene/UniProtKB:{}"
ALPHAFOLD_URL_TEMPLATE = "https://alphafold.ebi.ac.uk/entry/{}"
ORPHANET_URL_TEMPLATE = "https://www.orpha.net/es/disease/gene/{}"
PHARMGKB_SEARCH_URL_TEMPLATE = "https://www.pharmgkb.org/search?query={}"
GUIDETOPHARMACOLOGY_SEARCH_URL_TEMPLATE = "https://www.guidetopharmacology.org/GRAC/DatabaseSearchForward?searchString={}&searchCategories=all"

# URLs específicas de parsers
GUIDETOPHARMACOLOGY_TARGET_URL_TEMPLATE = "https://www.guidetopharmacology.org/GRAC/ObjectDisplayForward?objectId={}"
GUIDETOPHARMACOLOGY_LIGAND_URL_TEMPLATE = "https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId={}"
PANTHER_GO_URL_TEMPLATE = "http://www.pantherdb.org/panther/category.do?categoryAcc={}"
DRUGCENTRAL_SEARCH_URL_TEMPLATE = "https://drugcentral.org/drugcard/{}"
PANTHER_PATHWAY_URL_TEMPLATE = "https://pantherdb.org/pathway/pathwayDiagram.jsp?catAccession={}"
UNIPROT_LOCATION_URL_TEMPLATE = "https://www.uniprot.org/locations/{}"

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
            "Fuente": "PathwayCommons",
            "Enlace": PATHWAYCOMMONS_URL_TEMPLATE.format(search_term),
            "Descripción": "Base de datos de vías de señalización biológicas",
        },
        {
            "Fuente": "MalaCards",
            "Enlace": MALACARDS_URL_TEMPLATE.format(search_term),
            "Descripción": "Base de datos de enfermedades humanas",
        },
        {
            "Fuente": "Orphanet",
            "Enlace": ORPHANET_URL_TEMPLATE.format(search_term),
            "Descripción": "Portal de enfermedades raras y medicamentos huérfanos",
        },
        {
            "Fuente": "PharmGKB",
            "Enlace": PHARMGKB_SEARCH_URL_TEMPLATE.format(search_term),
            "Descripción": "Base de datos de farmacogenómica (búsqueda general)"
        },
        {
            "Fuente": "Guide to Pharmacology",
            "Enlace": GUIDETOPHARMACOLOGY_SEARCH_URL_TEMPLATE.format(search_term),
            "Descripción": "Base de datos de farmacología y objetivos moleculares",
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
            "Fuente": "UniProt",
            "Enlace": UNIPROT_INTERACTIONS_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Base de datos de interacciones moleculares - UniProt",
        },
        {
            "Fuente": "IntAct (EBI)",
            "Enlace": INTACT_EBI_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Base de datos de interacciones moleculares - EBI",
        },
        {
            "Fuente": "Functionome",
            "Enlace": FUNCTIONOME_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Análisis funcional basado en Gene Ontology",
        },
        {
            "Fuente": "AlphaFold",
            "Enlace": ALPHAFOLD_URL_TEMPLATE.format(uniprot_id),
            "Descripción": "Base de datos de estructuras proteicas predichas por IA",
        }
    ]