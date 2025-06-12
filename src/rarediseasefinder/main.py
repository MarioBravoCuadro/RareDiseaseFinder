import json

from tabulate import tabulate

from src.rarediseasefinder.biodata_providers.ensembl.EnsemblProcessor import EnsemblProcessor
from src.rarediseasefinder.biodata_providers.pantherdb.PantherProcessor import PantherProcessor
from src.rarediseasefinder.biodata_providers.pharos.PharosProcessor import PharosProcessor
from src.rarediseasefinder.biodata_providers.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from src.rarediseasefinder.biodata_providers.stringdb.StringDbProcessor import StringDbProcessor
from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor
from src.rarediseasefinder.biodata_providers.opentargets.OpenTargetsProcessor import OpenTargetsProcessor
from src.rarediseasefinder.biodata_providers.pharmgkb.PharmGKBProcessor import PharmGKBProcessor
from src.rarediseasefinder.biodata_providers.guidetopharmacology.PharmacologyProcessor import PharmacologyProcessor
from src.rarediseasefinder.biodata_providers.drugcentral.DrugCentralProcessor import DrugCentralProcessor
from src.rarediseasefinder.biodata_providers.ppiatlas.PPIAtlasProcessor import PPIAtlasProcessor


def process_data_source(processor_name, processor_class, filters_json):
    """
    Procesa datos de una fuente específica y muestra los resultados.
    
    Args:
        processor_name (str): Nombre de la fuente de datos (para mostrar en consola)
        processor_class (class): Clase del procesador a utilizar
        filters_json (dict): Filtros JSON para la consulta
    """
    print(f"\033[91m{processor_name}\033[0m")
    processor = processor_class()
    print(f"Status code {processor.get_status_code()}")
    
    if processor.get_status_code() == 200:
        results = processor.fetch(filters_json)
        if hasattr(results, "keys"):
            for key in results.keys():
                print(key)
                print(tabulate(results[key], headers='keys', tablefmt='fancy_grid'))


if __name__ == "__main__":
    filters_json = '''[
            {
                "PROCESSOR": "PharosProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "FANCA"}
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "df_info",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "df_omim",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "create_protein_protein_relations_df",
                        "FILTROS_METODO_PARSER": {
                            "PRIORIDAD_CLASES": {
                                "Tclin": 1,
                                "Tchem": 2,
                                "Tbio": 3,
                                "Tdark": 4
                            },
                            "PRIORIDAD_PROPIEDADES": {
                                "p_wrong": 1,
                                "p_ni": 2
                            }
                        }
                    },
                    {
                        "NOMBRE_METODO": "df_vias",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "df_numero_vias_por_fuente",
                        "FILTROS_METODO_PARSER": {}
                    }
                ]
            },
            {
                "PROCESSOR": "UniprotProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "O15360"}
                ],                
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "function",
                        "FILTROS_METODO_PARSER": ""
                    }
                    ,
                    {
                        "NOMBRE_METODO": "subcellular_location",
                        "FILTROS_METODO_PARSER": ""
                    }
                    ,
                    {
                        "NOMBRE_METODO": "go_terms",
                        "FILTROS_METODO_PARSER": ""
                    }
                    ,
                    {
                        "NOMBRE_METODO": "disease",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "disease_publications",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "parse_variants",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "parse_interactions",
                        "FILTROS_METODO_PARSER": ""
                    }
                ]
            },
            {
                "PROCESSOR": "SelleckchemProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "penicilina"}
                ],                
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "obtener_link_selleckchem",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "obtener_links_selleckchem",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "Funcion que da error",
                        "FILTROS_METODO_PARSER": ""
                    }
                ]
            },
            {
                "PROCESSOR": "EnsemblProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "FANCA"}
                ],                
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "ensembl_id",
                        "FILTROS_METODO_PARSER": ""
                    }
                ]
            },
            {
                "PROCESSOR": "OpenTargetsProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "ENSG00000118271"} 
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "basic_info",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "pathways",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "known_drugs",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "associated_diseases",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "interactions",
                        "FILTROS_METODO_PARSER": ""
                    },
                    {
                        "NOMBRE_METODO": "mouse_phenotypes",
                        "FILTROS_METODO_PARSER": ""
                    }
                ]
            },
            {
                "PROCESSOR": "PantherProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "P02766"}
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "annotation_name",
                        "FILTROS_METODO_PARSER": {}
                    }
                ]
            },
            {
                "PROCESSOR": "StringDbProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "ENSP00000360522"}
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "get_annotation",
                        "FILTROS_METODO_PARSER": {}
                    }
                ]
            }, {
                "PROCESSOR": "PharmGKBProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "FANCA"}
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "gene_symbols",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "label_annotations",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "literature",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "pathways",
                        "FILTROS_METODO_PARSER": {}
                    }
                ]
            },
            {
                "PROCESSOR": "PharmacologyProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "TTR"}
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "target_id",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "comments",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "references",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "interactions",
                        "FILTROS_METODO_PARSER": {}
                    }
                ]
            },
            {
                "PROCESSOR": "DrugCentralProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "tafamidis"}
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "drug_results",
                        "FILTROS_METODO_PARSER": {}
                    },
                    {
                        "NOMBRE_METODO": "drug_details",
                        "FILTROS_METODO_PARSER": {}
                    }
                ]
            },
            {
                "PROCESSOR": "PPIAtlasProcessor",
                "CLIENT_SEARCH_PARAMS": [
                    {"search_id": "TTR"}
                ],
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "ppi_table",
                        "FILTROS_METODO_PARSER": {}
                    }
                ]
            }
    ]'''
    filters_json = json.loads(filters_json)

    # Procesar todas las fuentes de datos usando la función
    process_data_source("OpenTargets", OpenTargetsProcessor, filters_json)
    process_data_source("SelleckChem", SelleckchemProcessor, filters_json)
    process_data_source("Pharos", PharosProcessor, filters_json)
    process_data_source("UniProt", UniprotProcessor, filters_json)
    process_data_source("Ensembl", EnsemblProcessor, filters_json)
    process_data_source("PantherDB", PantherProcessor, filters_json)
    process_data_source("StringDB", StringDbProcessor, filters_json)
    process_data_source("PharmGKB", PharmGKBProcessor, filters_json)
    process_data_source("Pharmacology", PharmacologyProcessor, filters_json)
    process_data_source("DrugCentral", DrugCentralProcessor, filters_json)
    process_data_source("PPIAtlas", PPIAtlasProcessor, filters_json)