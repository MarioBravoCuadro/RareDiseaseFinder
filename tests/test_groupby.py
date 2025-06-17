import json
from tabulate import tabulate
import pandas as pd
import os
from src.rarediseasefinder.biodata_providers.uniprot.UniprotProcessor import UniprotProcessor


def test_dataframe_grouping():
    """
    Prueba la funcionalidad de agrupación de DataFrames
    """
    print("Probando agrupación de DataFrames y conversión a JSON")
    print("-" * 50)
    
    # Crear una instancia del procesador a probar (Uniprot en este ejemplo)
    processor = UniprotProcessor()
    
    # Definir filtros con agrupación
    filters = [
        {
            "PROCESSOR": "UniprotProcessor",
            "CLIENT_SEARCH_PARAMS": {
                "search_id": "P02766"  # Transtiretina (ejemplo)
            },
            "METODOS_PARSER": [
                {
                    "NOMBRE_METODO": "disease_publications",  # Ajusta al método correcto
                    "FILTROS_METODO_PARSER": {
                        "group_by": "DiseaseID"  # Ajusta a la columna correcta
                    }
                },
                {
                    "NOMBRE_METODO": "go_terms",  # Otro método sin agrupación
                    "FILTROS_METODO_PARSER": {}
                }
            ]
        }
    ]
    
    try:
        # Obtener resultados
        print("Obteniendo datos...")
        results = processor.fetch(filters)
        
        # Mostrar estructura de resultados
        print("\nEstructura de resultados:")
        for method_name, result in results.items():
            if isinstance(result, pd.DataFrame):
                print(f"  - {method_name}: DataFrame único con {len(result)} filas")
            elif isinstance(result, list):
                print(f"  - {method_name}: Lista de {len(result)} DataFrames:")
                for i, df in enumerate(result):
                    group_value = df.attrs.get('group_value', f'grupo_{i+1}')
                    print(f"    * Grupo '{group_value}': {len(df)} filas")
            else:
                print(f"  - {method_name}: Otro tipo de datos: {type(result)}")
        
        # Convertir a JSON
        print("\nConvirtiendo a formato JSON...")
        json_results = processor.results_to_json(results)
        
        # Mostrar estructura JSON
        print("\nEstructura JSON:")
        for method_name, result in json_results.items():
            if isinstance(result, dict) and any(isinstance(v, list) for v in result.values()):
                print(f"  - {method_name}: Grupos JSON:")
                for group_key, items in result.items():
                    print(f"    * Grupo '{group_key}': {len(items)} items")
            elif isinstance(result, list):
                print(f"  - {method_name}: Lista JSON con {len(result)} items")
            else:
                print(f"  - {method_name}: Otro tipo de datos JSON: {type(result)}")
        
        # Guardar JSON en archivo para inspección
        file_path = os.path.join('tests', 'test_results.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2, ensure_ascii=False)
            print(f"\nResultados guardados en '{file_path}'")
        
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()



test_dataframe_grouping()