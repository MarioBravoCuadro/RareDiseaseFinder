from src.rarediseasefinder.pharos.PharosProcessor import PharosProcessor
from src.rarediseasefinder.selleckchem.SelleckchemProcessor import SelleckchemProcessor
from tabulate import tabulate

if __name__ == "__main__" :

    ##Call sellectChem processor
    processor = SelleckchemProcessor()
    dataframeLinksSellectChem =  processor.obtener_links_selleckchem("TCL")
    print(tabulate(dataframeLinksSellectChem, headers='keys', tablefmt='fancy_grid'))

    ##Call pharos processor
    processor = PharosProcessor()
    pharos_df_dict = processor.fetch("FANCA") #devuelve una lista de dataframes.
    print(type(pharos_df_dict))
    print(print(tabulate(pharos_df_dict, headers='keys', tablefmt='fancy_grid')))

    for dataFrame in pharos_df_dict:
        print(print(tabulate(pharos_df_dict[dataFrame], headers='keys', tablefmt='fancy_grid')))

