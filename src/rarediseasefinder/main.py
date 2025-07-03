import json
import pandas as pd

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
                print(f"\n\033[94m--- {key} ---\033[0m")
                result = results[key]
                
                # Caso 1: DataFrame único
                if isinstance(result, pd.DataFrame):
                    try:
                        print(tabulate(result, headers='keys', tablefmt='fancy_grid'))
                    except ValueError:
                        # Fallback si tabulate falla
                        print(result.to_string())
                
                # Caso 2: Lista de DataFrames (agrupados)
                elif isinstance(result, list) and all(isinstance(df, pd.DataFrame) for df in result):
                    # Si solo hay un DataFrame en la lista, mostrarlo directamente
                    if len(result) == 1:
                        try:
                            print(tabulate(result[0], headers='keys', tablefmt='fancy_grid'))
                        except ValueError:
                            # Fallback si tabulate falla
                            print(result[0].to_string())
                    else:
                        # Mostrar múltiples DataFrames con sus grupos
                        for i, df in enumerate(result):
                            group_name = df.attrs.get('group_value', f'Grupo {i+1}')
                            print(f"\n\033[92m** Grupo: {group_name} **\033[0m")
                            try:
                                print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
                            except ValueError:
                                # Fallback si tabulate falla
                                print(df.to_string())
                
                # Caso 3: Otro tipo de datos
                else:
                    print(f"Tipo de datos no soportado directamente: {type(result)}")
                    print(result)

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
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "subcellular_location",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "go_terms",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "disease",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "disease_publications",
                "FILTROS_METODO_PARSER": {
                    "group_by": "DiseaseID"
                }
            },
            {
                "NOMBRE_METODO": "variants",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "interactions",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "omim_references",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "external_links",
                "FILTROS_METODO_PARSER": {}
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
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "obtener_links_selleckchem",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "extraer_medicamentos",
                "FILTROS_METODO_PARSER": {}
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
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "external_links",
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
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "pathways",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "known_drugs",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "associated_diseases",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "interactions",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "mouse_phenotypes",
                "FILTROS_METODO_PARSER": {}
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
            },
            {
                "NOMBRE_METODO": "annotations",
                "FILTROS_METODO_PARSER": {}
            },
            {
                "NOMBRE_METODO": "pathways",
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
    }, 
    {
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
            {"search_id": "DOHH"}
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
    process_data_source("Ensembl", EnsemblProcessor, filters_json)
    process_data_source("DrugCentral", DrugCentralProcessor, filters_json)
    process_data_source("OpenTargets", OpenTargetsProcessor, filters_json)
    process_data_source("StringDB", StringDbProcessor, filters_json)
    process_data_source("SelleckChem", SelleckchemProcessor, filters_json)
    process_data_source("Pharos", PharosProcessor, filters_json)
    process_data_source("UniProt", UniprotProcessor, filters_json)
    process_data_source("PantherDB", PantherProcessor, filters_json)
    process_data_source("PharmGKB", PharmGKBProcessor, filters_json)
    process_data_source("Pharmacology", PharmacologyProcessor, filters_json)
    process_data_source("PPIAtlas", PPIAtlasProcessor, filters_json)