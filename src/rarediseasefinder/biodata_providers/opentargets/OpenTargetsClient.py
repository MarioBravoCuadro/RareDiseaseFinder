"""
Módulo de cliente para la API GraphQL de OpenTargets.
Proporciona métodos para consultar información de genes y dianas terapéuticas.
"""
from typing import Dict

import requests

from ...core.BaseClient import BaseClient
from ...core.errors import BaseParsingError


class OpenTargetsClient(BaseClient):
    """
    Cliente para interactuar con la API GraphQL de OpenTargets.
    Permite consultar información de genes por su ID de Ensembl.
    """
    
    GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"
    
    def _get_gene_query(self, ensembl_id: str) -> Dict[str, str]:
        """
        Construye la consulta GraphQL para obtener información de un gen por su ID de Ensembl.
        
        Args:
            ensembl_id (str): ID de Ensembl del gen a consultar.
            
        Returns:
            Dict[str, str]: Consulta GraphQL y variables.
        """
        query = """
        query GetGeneInfo($ensemblId: String!) {
            target(ensemblId: $ensemblId) {
                id
                approvedSymbol
                approvedName
                pathways {
                    pathwayId
                    pathway
                    topLevelTerm
                }
                knownDrugs {
                    rows {
                        drugId
                        prefName
                        mechanismOfAction
                        phase
                        disease {
                            name
                            id
                        }
                    }
                }
                associatedDiseases(page: {index: 0, size: 5}) {
                    rows {
                        disease {
                            id
                            name
                            description
                        }
                        score
                    }
                }
                interactions(scoreThreshold: 0.8, page: {index: 0, size: 30}) {
                    count
                    rows {
                        intA
                        intB
                        score
                    }
                }
                mousePhenotypes {
                    modelPhenotypeLabel
                    biologicalModels {
                        literature
                    }
                }
            }
        }
        """
        variables = {"ensemblId": ensembl_id}
        
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
    
    def fetch(self, id: str) -> dict:
        """
        Obtiene datos de un gen específico de OpenTargets.
        
        Args:
            id (str): ID de Ensembl del gen a consultar.
            
        Returns:
            dict: Datos del gen desde OpenTargets.
            
        Raises:
            BaseParsingError: Si la respuesta no contiene los datos esperados.
        """
        query_data = self._get_gene_query(id)
        response = self._query_graphql(query_data)
        
        try:
            response_data = response.json()
        except ValueError as e:
            raise BaseParsingError(f"Error al decodificar JSON: {str(e)}")
        
        if "data" in response_data and "target" in response_data["data"]:
            return response_data["data"]["target"]
        else:
            raise BaseParsingError(f"No se encontraron datos para el gen con ID Ensembl: {id}")
    
    def _ping_logic(self) -> int:
        """
        omprueba la versión de la base de datos de Pharos para verificar conectividad.
        Returns:
            int: Código de estado HTTP de la respuesta o 999 si falla la conexión.
        """
        test_query = {
            "query": 
            """
            query {
            meta {
                apiVersion { z, y, x }
                dataVersion { iteration, month, year }
                name
                }
            }
            """
        }   

        
        if self._try_connection(self.GRAPHQL_URL):
            response = self._query_graphql(test_query)
            return response.status_code
        else:
            return 999
    
    def check_data(self):
        """
        Verifica que los datos obtenidos sean válidos.
        
        Args:
            data (dict): Datos a verificar.
            
        Returns:
            bool: True si los datos son válidos, False en caso contrario.
        """
        pass
        