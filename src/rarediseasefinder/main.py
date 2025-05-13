import json

from tabulate import tabulate

from src.rarediseasefinder.biodata_providers.ensembl.EnsemblProcessor import EnsemblProcessor
from src.rarediseasefinder.biodata_providers.phanterdb.PhanterProcessor import PhanterProcessor
from src.rarediseasefinder.biodata_providers.pharos.PharosProcessor import PharosProcessor
from src.rarediseasefinder.biodata_providers.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from src.rarediseasefinder.biodata_providers.stringdb.StringDbProcessor import StringDbProcessor
from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor
from src.rarediseasefinder.biodata_providers.opentargets.OpenTargetsProcessor import OpenTargetsProcessor

if __name__ == "__main__" :
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
                    {"search_id": "TCL"}
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
                "PROCESSOR": "PhanterProcessor",
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
            }
            
    ]'''
    filters_json = json.loads(filters_json)

        
    #Call OpenTargets processor
    print("\033[91mOpenTargets\033[0m")
    processor = OpenTargetsProcessor()
    print("Status code " + str(processor.get_status_code()))
    if processor.get_status_code() == 200:
        open_targets_id = processor.fetch(filters_json)
        for dataFrame in open_targets_id:
            print(dataFrame)
            print(tabulate(open_targets_id[dataFrame], headers='keys', tablefmt='fancy_grid'))
        
    ##Call sellectChem processor
    print("\033[91msellectChem\033[0m")
    processor = SelleckchemProcessor()
    print("Status code " + str(processor.get_status_code()))
    dataframeLinksSellectChem = processor.fetch(filters_json)
    for dataFrame in dataframeLinksSellectChem:
        print(dataFrame)
        print(tabulate(dataframeLinksSellectChem[dataFrame],headers='keys', tablefmt='fancy_grid'))

    ##Call pharos processor
    print("\033[91mpharos\033[0m")
    processor = PharosProcessor()
    print("Status code " + str(processor.get_status_code()))
    if processor.get_status_code() == 200:
        pharos_df_dict = processor.fetch(filters_json) #devuelve una lista de dataframes.
        #print(pharos_df_dict.keys())
        #print(tabulate(pharos_df_dict, headers='keys', tablefmt='fancy_grid'))

        for dataFrame in pharos_df_dict:
            print(dataFrame)
            print(tabulate(pharos_df_dict[dataFrame], headers='keys', tablefmt='fancy_grid'))

    ##Call Uniprot processor
    print("\033[91mUniProt\033[0m")
    processor = UniprotProcessor()
    print("Status code " + str(processor.get_status_code()))
    if processor.get_status_code() == 200:
        uniprot_dict = processor.fetch(filters_json) #Fanca
        print(uniprot_dict.keys())
        for key in uniprot_dict.keys():
            print(key)
            print(tabulate(uniprot_dict[key], headers='keys', tablefmt='fancy_grid'))

    #Call Ensembl processor
    print("\033[91mEnsembl\033[0m")
    processor = EnsemblProcessor()
    print("Status code " + str(processor.get_status_code()))
    if processor.get_status_code() == 200:
        ensembl_id = processor.fetch(filters_json)
        print(tabulate(ensembl_id, headers='keys', tablefmt='fancy_grid'))

    #Call PhanterDB processor
    print("\033[91mPhantherDB\033[0m")
    processor = PhanterProcessor()
    print("Status code " + str(processor.get_status_code()))
    if processor.get_status_code() == 200:
        phanter_data = processor.fetch(filters_json)
        print(tabulate(phanter_data, headers='keys', tablefmt='fancy_grid'))

    #Call StringDB processor
    print("\033[91mStringDB\033[0m")
    processor = StringDbProcessor()
    print("Status code " + str(processor.get_status_code()))
    if processor.get_status_code() == 200:
        string_db = processor.fetch(filters_json) #Fanca
        print(string_db.keys())
        for key in string_db.keys():
            print(key)
            print(tabulate(string_db[key], headers='keys', tablefmt='fancy_grid'))
