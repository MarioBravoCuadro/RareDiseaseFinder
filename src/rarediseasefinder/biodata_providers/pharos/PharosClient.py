from typing import Dict, Tuple

import requests

from ...core.BaseClient import BaseClient
from ...core.errors import BaseParsingError


class PharosClient(BaseClient):
    """
    Cliente para interactuar con la API GraphQL de Pharos.
    Permite construir consultas, ejecutarlas y obtener datos de targets específicos.
    """
    
    GRAPHQL_URL = "https://pharos-api.ncats.io/graphql"

    def _get_pharos_query(self, target: str) -> Tuple[str, Dict[str, str]]:
        """
        Construye la consulta GraphQL para obtener información de un target por su símbolo.
        
        Args:
            target (str): Símbolo del target a consultar.
            
        Returns:
            Tuple[str, Dict[str, str]]: Consulta GraphQL lista para enviar y las variables.
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
        
        return query, variables
    
    def _query_graphql(self, query: str, variables: Dict[str, str]=None) -> requests.Response:
        """
        Ejecuta una consulta GraphQL en la API de Pharos.
        
        Args:
            query (str): Consulta GraphQL a ejecutar.
            variables (Dict[str, str]): Variables para la consulta GraphQL.
            
        Returns:
            Dict[str, Any]: Datos JSON de la respuesta.
        """
        payload = {"query": query}
        if variables is not None:
            payload["variables"] = variables
        response = self._post_data(self.GRAPHQL_URL, json=payload)
        return response

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

        query,variables = self._get_pharos_query(target)
        response_data = self._query_graphql(query,variables).json()
        
        if "data" in response_data and "target" in response_data["data"]:
            return response_data["data"]["target"]
        else:
            raise BaseParsingError(f"No se encontraron datos para el objetivo: {target}")
        
    def _ping_logic(self) -> int:
        query = "query { dbVersion }"

        if self._try_connection(self.GRAPHQL_URL):
            response = self._query_graphql(query=query)
            return response.status_code
        else:
            return 999
        
    def check_data(self):
        raise NotImplementedError("Método check_data no implementado en PharosClient.")