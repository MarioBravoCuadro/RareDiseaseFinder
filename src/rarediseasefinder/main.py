from src.rarediseasefinder.pharos.PharosProcessor import PharosProcessor
from src.rarediseasefinder.selleckchem.SelleckchemProcessor import SelleckchemProcessor

if __name__ == "__main__" :

    ##Call sellectChem processor
    processor = SelleckchemProcessor()
    dataframeLinksSellectChem =  processor.obtener_links_selleckchem("TCL")
    print(dataframeLinksSellectChem)

    ##Call pharos processor
    processor = PharosProcessor()
    pharos_df = processor.fetch("FANCA")
    print(pharos_df)
