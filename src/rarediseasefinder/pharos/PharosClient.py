from typing import Dict
from ..core.errors import BaseParsingError
from ..core.client import BaseClient

class PharosClient(BaseClient):
    """Cliente para interactuar con la API GraphQL de Pharos"""
    
    GRAPHQL_URL = "https://pharos-api.ncats.io/graphql"

    def get_uniprot_query(self, target: str) -> str:
        query = f"""
            query ObtenerInfoVariante {{
            target(q: {{ sym: "{target}" }}) {{
                nombre: name
                uniprot_ID: uniprot
                descripcion: description
                claseDiana: tdl
                secuencia: seq

                referenciaOMIM: mim {{
                OMIM_ID: mimid
                nombre: term
                }}

                ligandosConocidos: ligands {{
                nombre: name
                ligando_ID: ligid
                }}

                deLosCualesSonFarmacosAprobados: ligands(isdrug: true) {{
                nombre: name
                ligando_ID: ligid
                }}

                relacionProteinaProteina: ppis{{
                target {{
                    nombre: name
                    proteina_ID: sym
                    secuencia: seq
                    claseDiana: tdl
                }}
                propiedadesRelacion: props {{
                    name
                    value
                }}
                }}

                numeroDeViasPorFuente: pathwayCounts {{
                fuente: name
                numVias: value
                }}

                vias: pathways {{
                viaPharos_ID: pwid
                nombre: name
                fuente: type
                fuente_ID: sourceID
                url
                }}
            }}
            }}
        """
        return query
    
    def query_graphql(self, query: str) -> Dict:
        """
        Ejecuta una consulta GraphQL en la API de Pharos
        
        Args:
            query (str): Consulta GraphQL a ejecutar
            variables (dict, optional): Variables para la consulta GraphQL
            
        Returns:
            dict: Datos JSON de la respuesta
        """
        payload = {"query": query}
    
        return self._post_data(self.GRAPHQL_URL, json=payload)
    
    def get_target_data(self, target: str) -> Dict:
        """
        Obtiene datos de un objetivo específico de Pharos
        
        Args:
            target (str): Símbolo del objetivo a consultar
            
        Returns:
            dict: Datos del objetivo desde Pharos
            
        Raises:
            BaseParsingError: Si la respuesta no contiene los datos esperados
        """

        query = self.get_uniprot_query(target)
        response_data = self.query_graphql(query)
        
        if "data" in response_data and "target" in response_data["data"]:
            return response_data["data"]["target"]
        else:
            raise BaseParsingError(f"No se encontraron datos para el objetivo: {target}")