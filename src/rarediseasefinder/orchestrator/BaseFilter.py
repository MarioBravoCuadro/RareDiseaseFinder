import json

class BaseFilter:

    def __init__(self, minium_methods, processor_id):
        self.minium_methods = minium_methods
        self.processor_id = processor_id
        self.create_base_tree()
        self.add_processor_to_filter(processor_id)
        self.add_minium_methods()

    def create_base_tree(self):
        self.json_filter = {
            "PROCESSOR": None,
            "CLIENT_SEARCH_PARAMS": [],
            "METODOS_PARSER": []
        }

    def add_processor_to_filter(self, processor_id):
        self.json_filter["PROCESSOR"] = processor_id

    def add_client_search_params(self, search_id):
        self.json_filter["CLIENT_SEARCH_PARAMS"] = [{"search_id": search_id}]

    def add_parser_method(self, method_id, parser_method_filters):
        self.json_filter["METODOS_PARSER"].append({
            "NOMBRE_METODO": method_id,
            "FILTROS_METODO_PARSER": parser_method_filters
        })

    def add_minium_methods(self):
        for method in self.minium_methods:
            self.add_parser_method(method["METHOD_ID"], method["METHOD_PARSER_FILTERS"])

    def get_json(self):
        return json.dumps(self.json_filter, indent=4)