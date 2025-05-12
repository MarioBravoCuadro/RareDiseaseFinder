"""
Módulo de cliente para la API GraphQL de Pharos.
Proporciona clases y métodos para construir y ejecutar consultas GraphQL y obtener datos de targets.
"""
from typing import Dict

import requests

from ...core.BaseClient import BaseClient
from ...core.errors import BaseParsingError


class PharosClient(BaseClient):
    """
    Cliente para interactuar con la API GraphQL de Pharos.
    Permite construir consultas, ejecutarlas y obtener datos de targets específicos.
    """
    
    GRAPHQL_URL = "https://pharos-api.ncats.io/graphql"

    def _get_pharos_query(self, target: str) -> Dict[str, str]:
        """
        Construye la consulta GraphQL para obtener información de un target por su símbolo.
        
        Args:
            target (str): Símbolo del target a consultar.
            
        Returns:
            Dict[str, str]: Consulta GraphQL y variables.
        """
        query = """
            query GetGeneInfo($target: String!) {
                target(q: { sym: $target }) {
                    nombre: name
                    uniprot_ID: uniprot
                    descripcion: description
                    claseDiana: tdl
                    secuencia: seq

                    referenciaOMIM: mim {
                        OMIM_ID: mimid
                        nombre: term
                    }

                    ligandosConocidos: ligands {
                        nombre: name
                        ligando_ID: ligid
                    }

                    deLosCualesSonFarmacosAprobados: ligands(isdrug: true) {
                        nombre: name
                        ligando_ID: ligid
                    }

                    relacionProteinaProteina: ppis {
                        target {
                            nombre: name
                            proteina_ID: sym
                            secuencia: seq
                            claseDiana: tdl
                        }
                        propiedadesRelacion: props {
                            name
                            value
                        }
                    }

                    numeroDeViasPorFuente: pathwayCounts {
                        fuente: name
                        numVias: value
                    }

                    vias: pathways {
                        viaPharos_ID: pwid
                        nombre: name
                        fuente: type
                        fuente_ID: sourceID
                        url
                    }
                }
            }
        """
        variables = {"target": target}
        
        return {"query": query, "variables": variables}
    
    def _query_graphql(self, query_data: Dict) -> requests.Response:
        """
        Ejecuta una consulta GraphQL en la API de Pharos.
        
        Args:
            Dict: Datos de la consulta GraphQL.
                Query: Consulta GraphQL.
                Variables: Variables para la consulta.

        Returns:
            Dict[str, Any]: Datos JSON de la respuesta.

        Raises:
            BaseHTTPError: Si hay problemas en la comunicación HTTP.
        """
        return self._post_data(self.GRAPHQL_URL, json=query_data)

    def get_target_data(self, target: str) -> dict:
        """
        Obtiene datos de un objetivo específico de Pharos.
        
        Args:
            target (str): Símbolo del objetivo a consultar.
            
        Returns:
            dict: Datos del objetivo desde Pharos.
            
        Raises:
            BaseParsingError: Si la respuesta no contiene los datos esperados.
        """

        query_data = self._get_pharos_query(target)
        response = self._query_graphql(query_data)
        
        try:
            response_data = response.json()
        except ValueError as e:
            raise BaseParsingError(f"Error al decodificar JSON: {str(e)}")
        
        if "data" in response_data and "target" in response_data["data"]:
            return response_data["data"]["target"]
        else:
            raise BaseParsingError(f"No se encontraron datos para el gen con ID Ensembl: {target}")
        
    def _ping_logic(self) -> int:
        """
        Comprueba la versión de la base de datos de Pharos para verificar conectividad.
        Returns:
            int: Código de estado HTTP de la respuesta o 999 si falla la conexión.
        """
        query_data = {
            "query": "query { dbVersion }",
            "variables": {}
        }

        if self._try_connection(self.GRAPHQL_URL):
            response = self._query_graphql(query_data)
            return response.status_code
        else:
            return 999
        
    def check_data(self):
        """
        Placeholder para lógica de validación de los datos obtenidos de Pharos.
        """
        pass