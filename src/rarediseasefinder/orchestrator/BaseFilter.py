import json

from numpy.ma.core import minimum


class BaseFilter:

    minium_methods = None
    processor_id = None
    json_filter = ''''''

    def __init__(self,minium_methods,processor_id):
        self.minium_methods = minium_methods
        self.processor_id  = processor_id
        self.add_minium_methods()

    def create_base_tree(self):
         self.json_filter = json.dumps({"PROCESSOR": None, "CLIENT_SEARCH_PARAMS": [], "METODOS_PARSER": []},indent=6)

    def add_processor_to_filter(self,processor_id):
        intermediate_json_filter = json.loads(self.json_filter)
        intermediate_json_filter["PROCESSOR"] = processor_id
        self.json_filter = str(intermediate_json_filter)

    def add_client_search_params(self,search_id):
        intermediate_json_filter = json.loads(self.json_filter)
        intermediate_json_filter["CLIENT_SEARCH_PARAMS"] = {"search_id": search_id}
        self.json_filter = str(intermediate_json_filter)

    def add_parser_method(self,method_id, parser_method_filters):
        intermediate_json_filter = json.loads(self.json_filter)
        intermediate_json_filter["METODOS_PARSER"].append({"NOMBRE_METODO" : method_id , "FILTROS_METODO_PARSER" : parser_method_filters})
        self.json_filter = str(intermediate_json_filter)

    def add_minium_methods(self):
        for method in self.minium_methods:
            self.add_parser_method(method["METHOD_ID"],method["METHOD_PARSER_FILTERS"])
