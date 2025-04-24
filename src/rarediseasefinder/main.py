from src.rarediseasefinder.ensembl.EnsemblProcessor import EnsemblProcessor
from src.rarediseasefinder.pharos.PharosProcessor import PharosProcessor
from src.rarediseasefinder.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from tabulate import tabulate

from src.rarediseasefinder.uniprot.UniprotProcessor import UniprotProcessor

if __name__ == "__main__" :

    ##Call sellectChem processor
    processor = SelleckchemProcessor()
    dataframeLinksSellectChem =  processor.obtener_links_selleckchem("TCL")
    print(tabulate(dataframeLinksSellectChem, headers='keys', tablefmt='fancy_grid'))

    ##Call pharos processor
    processor = PharosProcessor()
    pharos_df_dict = processor.fetch("FANCA") #devuelve una lista de dataframes.
    print(pharos_df_dict.keys())
    print(tabulate(pharos_df_dict, headers='keys', tablefmt='fancy_grid'))

    for dataFrame in pharos_df_dict:
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
