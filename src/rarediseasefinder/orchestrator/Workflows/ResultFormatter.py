from typing import List, Dict, Any, Tuple, Optional
import pandas as pd

from src.rarediseasefinder.orchestrator.Workflows.DataframesUtils import DataframesUtils

class ResultFormatter:
    """
    Clase para formatear resultados de workflows en una estructura JSON jerárquica.
    Permite mapear resultados a categorías según configuraciones específicas por workflow.
    """
    
    @staticmethod
    def format_workflow_results(
        results: List[Tuple[str, Any, str]], 
        category_config: Dict[str, Dict[str, Any]],
        method_category_mapping: Dict[str, str],
        grouping_config: Dict[str, Optional[str]] = None
    ) -> Dict[str, Any]:
        """
        Formatea los resultados del workflow en la estructura JSON jerárquica requerida.
        
        Args:
            results: Lista de tuplas (step_name, resultado, method_id)
            category_config: Configuración de las categorías disponibles
            method_category_mapping: Mapeo de métodos a categorías
            grouping_config: Configuración para agrupar dataframes (method_id -> column_name)
            
        Returns:
            Estructura JSON con categorías y subcategorías
        """
        # Inicializar estructura de categorías
        categories_dict = {}
        
        # Inicializar contadores de subcategorías por categoría
        subcategory_counters = {}
        
        # Si no hay configuración de agrupación, inicializar vacía
        if grouping_config is None:
            grouping_config = {}
        
        # Procesar cada resultado
        for step_name, result, method_id in results:
            # Determinar a qué categoría pertenece este método
            category_id = method_category_mapping.get(method_id)
            
            # Si no hay mapeo específico para este método, continuar con el siguiente resultado
            if not category_id or category_id not in category_config:
                continue
                
            # Obtener información de la categoría
            category_info = category_config[category_id]
            
            # Inicializar contador si es necesario
            if category_id not in subcategory_counters:
                subcategory_counters[category_id] = 0
            
            # Asegurarse de que la categoría existe
            if category_id not in categories_dict:
                categories_dict[category_id] = {
                    "id": category_id,
                    "title": category_info['title'],
                    "content": []
                }
            
            # Incrementar contador para esta categoría
            subcategory_counters[category_id] += 1
            
            # Generar ID de subcategoría
            subcategory_id = f"{category_id}.{subcategory_counters[category_id]}"
            
            # Verificar si este método requiere agrupación
            group_column = grouping_config.get(method_id)
            
            # Si es un DataFrame y requiere agrupación, procesarlo como un conjunto de grupos
            if isinstance(result, pd.DataFrame) and group_column is not None:
                # Agrupar el DataFrame
                grouped_dfs = DataframesUtils.group_dataframe(result, group_column)
                
                # Si solo hay un grupo o no se pudo agrupar, tratarlo como un DataFrame regular
                if len(grouped_dfs) <= 1:
                    processed_data = DataframesUtils.dataframe_to_json(result)
                    
                    # Añadir como subcategoría regular
                    categories_dict[category_id]['content'].append({
                        "id": subcategory_id,
                        "title": method_id,
                        "content": processed_data
                    })
                else:
                    # Crear una subcategoría para contener los grupos
                    subcategory = {
                        "id": subcategory_id,
                        "title": method_id,
                        "content": []
                    }
                    
                    # Procesar cada grupo como un elemento en la subcategoría
                    for i, group_df in enumerate(grouped_dfs, 1):
                        group_title = f"{group_df.attrs.get('group_value', f'Grupo {i}')}"
                        group_id = f"{subcategory_id}.{i}"
                        
                        # Convertir este grupo a JSON
                        group_data = DataframesUtils.dataframe_to_json(group_df)
                        
                        # Añadir como item dentro de la subcategoría
                        subcategory['content'].append({
                            "id": group_id,
                            "title": group_title,
                            "content": group_data
                        })
                    
                    # Añadir la subcategoría a la categoría principal
                    categories_dict[category_id]['content'].append(subcategory)
            else:
                # Para resultados que no requieren agrupación
                processed_data = DataframesUtils.dataframe_to_json(result)
                
                # Añadir como subcategoría regular
                categories_dict[category_id]['content'].append({
                    "id": subcategory_id,
                    "title": method_id,
                    "content": processed_data
                })
        
        # Convertir diccionario de categorías a lista ordenada por ID
        categories_list = sorted(
            categories_dict.values(), 
            key=lambda x: int(x['id']) if x['id'].isdigit() else x['id']
        )
        
        return {"categories": categories_list}