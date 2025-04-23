
from src.rarediseasefinder.selleckchem.SelleckchemProcessor import SelleckchemProcessor

if __name__ == "__main__" :

    ##Call sellectChem processor
    processor = SelleckchemProcessor()
    dataframeLinksSellectChem =  processor.obtener_link_selleckchem("TCL")
    print(dataframeLinksSellectChem)