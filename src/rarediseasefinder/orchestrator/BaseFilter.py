import json
from typing import List, Dict, Any

class BaseFilter:
    """
    Base class for creating JSON filters for the orchestrator.

    Attributes:
        minium_methods (list): A list of minimum methods to be included in the filter.
        processor_id (str): The ID of the processor.
        json_filter (dict): The dictionary representing the JSON filter.
    """

    def __init__(self, minium_methods: List[Dict[str, Any]], processor_id: str) -> None:
        """
        Initializes the BaseFilter with minimum methods and processor ID.

        Args:
            minium_methods (list): A list of minimum methods.
            processor_id (str): The ID of the processor.
        """
        self.minium_methods = minium_methods
        self.processor_id = processor_id
        self.create_base_tree()
        self.add_processor_to_filter(processor_id)
        self.add_minium_methods()

    def create_base_tree(self) -> None:
        """Creates the basic structure of the JSON filter."""
        self.json_filter = {
            "PROCESSOR": None,
            "CLIENT_SEARCH_PARAMS": [],
            "METODOS_PARSER": []
        }

    def add_processor_to_filter(self, processor_id: str) -> None:
        """
        Adds the processor ID to the JSON filter.

        Args:
            processor_id (str): The ID of the processor.
        """
        self.json_filter["PROCESSOR"] = processor_id

    def add_client_search_params(self, search_id: str) -> None:
        """
        Adds client search parameters to the JSON filter.

        Args:
            search_id (str): The search ID.
        """
        self.json_filter["CLIENT_SEARCH_PARAMS"] = [{"search_id": search_id}]

    def add_parser_method(self, method_id: str, parser_method_filters: List[Any]) -> None:
        """
        Adds a parser method to the JSON filter.

        Args:
            method_id (str): The ID of the method.
            parser_method_filters (list): A list of filters for the parser method.
        """
        self.json_filter["METODOS_PARSER"].append({
            "NOMBRE_METODO": method_id,
            "FILTROS_METODO_PARSER": parser_method_filters
        })

    def add_minium_methods(self) -> None:
        """Adds the minimum required methods to the parser methods list."""
        for method in self.minium_methods:
            self.add_parser_method(method["METHOD_ID"], method["METHOD_PARSER_FILTERS"])

    def get_json_str(self) -> str:
        """
        Returns the JSON filter as a JSON formatted string.

        Returns:
            str: The JSON filter formatted as a string.
        """
        return json.dumps(self.json_filter, indent=4)