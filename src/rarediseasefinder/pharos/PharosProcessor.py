from .PharosClient import PharosClient
from .PharosParser import PharosParser

class PharosProcessor:

    pharosClient = None
    pharosParser = None

    def __init__(self):
        self.pharosClient = PharosClient()
        self.pharosParser = PharosParser()

    filters =[
            {
                "procesador":"Pharos",
                "prioridad_clases":{
                    "Tclin": 1,
                    "Tchem": 2,
                    "Tbio": 3,
                    "Tdark": 4
                },
                "prioridad_propiedades":{
                    "p_wrong": 1,
                    "p_ni": 2
                    # "p_int": 3,
                    # "novelty": 4
                }
            },
            {
                "procesador": "Uniprot",
            },
            {
                "procesador": "Selleckchem",
            }

    ]

    def getFilters(self, filters: list):
        global filtros
        for processor in filters:
            if processor["procesador"] == "Pharos":
                prioridad_clases = processor["prioridad_clases"]
                prioridad_propiedades = processor["prioridad_propiedades"]

                filtros: {
                    "prioridad_clases": prioridad_clases,
                    "prioridad_propiedades": prioridad_propiedades
                }
                return filtros
            else:
                return None
        pass

    def fetch(self, identifier:str):

        filters = self.getFilters(self.filters)
        prioridad_clases = filters["prioridad_clases"]
        prioridad_propiedades = filters["prioridad_propiedades"]
        data = self.pharosClient.get_target_data(identifier)
        if data :
            pharos_dataframes = self.pharosParser.parse(data,prioridad_clases,prioridad_propiedades)
            return  pharos_dataframes




