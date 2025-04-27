import json

from src.rarediseasefinder.biodata_providers.ensembl.EnsemblProcessor import EnsemblProcessor
from src.rarediseasefinder.biodata_providers.pharos.PharosProcessor import PharosProcessor
from src.rarediseasefinder.biodata_providers.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor

from tabulate import tabulate

if __name__ == "__main__" :
    filters_json = '''[
            {
                "PROCESSOR": "PharosProcessor",
                "SEARCH_PARAMS": [
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
                "PROCESSOR": "SelleckchemProcessor",
                "METODOS_PARSER": [
                    {
                        "NOMBRE_METODO": "createaa_df",
                        "FILTROS_METODO_PARSER": {

                        }
                    },
                    {
                        "NOMBRE_METODO": "metodo2",
                        "FILTROS_METODO_PARSER": "filtro2"
                    }
                ]
            }
        ]'''

    ##Call sellectChem processor
    processor = SelleckchemProcessor()
    dataframeLinksSellectChem =  processor.obtener_links_selleckchem("TCL")
    print(tabulate(dataframeLinksSellectChem, headers='keys', tablefmt='fancy_grid'))

    ##Call pharos processor
    processor = PharosProcessor()
    pharos_df_dict = processor.fetch(json.loads(filters_json)) #devuelve una lista de dataframes.
    #print(pharos_df_dict.keys())
    #print(tabulate(pharos_df_dict, headers='keys', tablefmt='fancy_grid'))

    for dataFrame in pharos_df_dict:
        print(dataFrame)
        print(tabulate(pharos_df_dict[dataFrame], headers='keys', tablefmt='fancy_grid'))

    ##Call Uniprot processor
    processor = UniprotProcessor()
    uniprot_dict = processor.get_uniprot_data("O15360") #Fanca
    print(uniprot_dict.keys())
    for key in uniprot_dict.keys():
        print(key)
        print(tabulate(uniprot_dict[key], headers='keys', tablefmt='fancy_grid'))

    #Call Ensembl processor
    processor = EnsemblProcessor()
    ensembl_id = processor.get_ensembl_id("FANCA")
    print("ensembl_id: " + ensembl_id)
