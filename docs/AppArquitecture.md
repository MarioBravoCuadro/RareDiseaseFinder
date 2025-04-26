# Diagrama de clases de la aplicación

```mermaid
---
config:
  layout: elk
  theme: dark
---
classDiagram
    namespace controller{
    class Orchestrator {
        +run(selected_sources: List~str~, identifier: str): Dict~str, Dict~str, DataFrame~~
        -_process_enrichments(data: DataFrame, enrichers: List~EnrichmentProcessor~): DataFrame~
    }
    }
    namespace core {
        class BaseClient {
            +fetch_data(url, params, headers) Dict
        }
        class BaseParser {
            +parse_to_dataframe(data) DataFrame
        }
        class BaseWebScraper {
            +scrape_url(url) String
        }
        class Constants {

        }
        class Utils {

        }
        class Errors {

        }
    }
    namespace pharos {
        class PharosProcessor {
            +fetch(identifier: str): Dict~str, DataFrame~
        }
        class PharosClient {
            -GRAPHQL_URL: String
            +query_graphql(query) Dict
        }
        class PharosParser {
            +parse_all(data) Dict~DataFrame~
        }
    }
    namespace uniprot {
        class UniProtProcessor {
            +fetch(identifier: str): Dict~str, DataFrame~
        }
        class UniProtClient {
            -BASE_URL: String
            +get_by_id(uniprot_id) Dict
        }
        class UniProtParser {
            +parse_all(data) Dict~DataFrame~
        }
    }
    namespace selleckchem {
        class SelleckchemScraper {
            -SEARCH_URL: String
            +extract_drug_info(html) List~Dict~
        }
        class SelleckChemProcessor {

        }
        class SelleckChemParser {

        }
    }

    namespace ensembl{
        class EnsemblClient{

        }
        class EnsemblParser{

        }
        class EnsemblProcessor{

        }
    }

    namespace processers{
        class DataSource {
            <<Interface>>
            +fetch(identifier: str): Dict~str, DataFrame~
        }
        class EnrichmentProcessor {
            <<Interface>>
            +enrich(data: DataFrame): DataFrame~
        }
        class PostProcessor {
            +process(data: DataFrame, enrichers: List~EnrichmentProcessor~): DataFrame~
        }
    }

PharosProcessor --> PharosClient
PharosProcessor --> PharosParser
DataSource <|.. PharosProcessor
BaseClient <|-- PharosClient
BaseParser <|-- PharosParser

Orchestrator --> DataSource
Orchestrator --> PostProcessor
PostProcessor --> EnrichmentProcessor

UniProtProcessor --> UniProtClient
UniProtProcessor --> UniProtParser
DataSource <|.. UniProtProcessor
BaseClient <|-- UniProtClient
BaseParser <|-- UniProtParser

SelleckChemProcessor --> SelleckChemParser
DataSource <|.. SelleckChemProcessor
BaseParser <|-- SelleckChemParser
SelleckChemProcessor --> SelleckchemScraper
BaseWebScraper <|-- SelleckchemScraper

EnsemblProcessor --> EnsemblClient
EnsemblProcessor --> EnsemblParser
DataSource <|.. EnsemblProcessor
BaseClient <|-- EnsemblClient
BaseParser <|-- EnsemblParser