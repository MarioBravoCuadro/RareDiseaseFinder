import json
from abc import ABCMeta
from abc import abstractmethod
class IWorkflow(metaclass=ABCMeta):
    @abstractmethod
    def get_steps(self):
        pass
    @abstractmethod
    def check_if_all_steps_available(self):
        pass

    def get_json_from_route(self,route):
        with open(route, 'r') as file:
            data = json.load(file)
        return data

    def add_search_id_to_json(self,json_file, search_id):
        json_file["CLIENT_SEARCH_PARAMS"][0]["search_id"] = search_id
        return json_file