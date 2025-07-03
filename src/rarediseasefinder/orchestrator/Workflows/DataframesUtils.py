from typing import Union, List, Dict, Any

import pandas as pd


class DataframesUtils:
    @staticmethod
    def group_dataframe(df: pd.DataFrame, group_column: str = None) -> List[pd.DataFrame]:
        """
        Agrupa un DataFrame por una columna específica y añade un subíndice a cada grupo.

        Args:
            df (pd.DataFrame): DataFrame a agrupar.
            group_column (str, optional): Columna para agrupar.

        Returns:
            List[pd.DataFrame]: Lista de DataFrames agrupados, cada uno con una columna 'subindice'.
        """
        # Si el DataFrame está vacío o no hay columna de agrupación, devolver lista con el DataFrame original
        if df.empty or not group_column or group_column not in df.columns:
            return [df]

        # Agrupar por la columna especificada
        grouped_dfs = []
        for name, group in df.groupby(group_column):
            # Resetear índices para consistencia
            group_df = group.reset_index(drop=True)
            # Añadir metadato para identificar el grupo
            group_df.attrs['group_value'] = name
            # Añadir columna de subíndice
            group_df['subindice'] = group_df.index + 1
            grouped_dfs.append(group_df)

        return grouped_dfs

    @staticmethod
    def results_to_json(results: Union[Dict[str, Union[pd.DataFrame, List[pd.DataFrame]]], List[Union[pd.DataFrame, List[pd.DataFrame]]]]) -> Dict[str, Any]:
        """
        Convierte los resultados a formato JSON usando los métodos estáticos de la clase.
        Puede aceptar un diccionario o una lista de resultados.

        Args:
            results (Union[Dict[str, Union[pd.DataFrame, List[pd.DataFrame]]], List[Union[pd.DataFrame, List[pd.DataFrame]]]]): Resultados procesados.

        Returns:
            Dict[str, Any]: Resultados en formato JSON.
        """
        json_results = {}
        if isinstance(results, dict):
            items = results.items()
        elif isinstance(results, list):
            items = [(f'result_{i}', res) for i, res in enumerate(results)]
        else:
            return json_results
        for method_name, result in items:
            json_results[method_name] = DataframesUtils.dataframe_to_json(result)
        return json_results

    @staticmethod
    def dataframe_to_json(data) -> Any:
        """
        Convierte recursivamente DataFrames, listas de DataFrames o diccionarios anidados a formato JSON serializable.

        Args:
            data: DataFrame, lista, diccionario o cualquier estructura anidada.

        Returns:
            Estructura de datos JSON serializable.
        """
        import pandas as pd
        if isinstance(data, pd.DataFrame):
            return data.to_dict(orient='records')
        elif isinstance(data, list):
            return [DataframesUtils.dataframe_to_json(item) for item in data]
        elif isinstance(data, dict):
            return {k: DataframesUtils.dataframe_to_json(v) for k, v in data.items()}
        else:
            return data

    @staticmethod
    def create_dataframe(df_list: List[Union[dict, pd.DataFrame]]) -> pd.DataFrame:
        """
        Une múltiples elementos en un solo DataFrame.
        
        Si recibe una lista de DataFrames, los concatena.
        Si recibe una lista de diccionarios, crea un nuevo DataFrame.

        Args:
            df_list (List[Union[dict, pd.DataFrame]]): Lista de elementos a unir.

        Returns:
            pd.DataFrame: DataFrame resultante de la unión.
        """
        if not df_list:
            return pd.DataFrame()
            
        # Verificar si son DataFrames o diccionarios
        if all(isinstance(item, pd.DataFrame) for item in df_list):
            # Si son todos DataFrames, concatenarlos
            return pd.concat(df_list, ignore_index=True)
        else:
            # Si son diccionarios u otros tipos, usar el constructor de DataFrame
            return pd.DataFrame(df_list)
        
    @staticmethod
    def dataframe_to_dict(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Convierte un DataFrame a un diccionario con una estructura anidada.

        Args:
            df (pd.DataFrame): DataFrame a convertir.

        Returns:
            Dict[str, Any]: Diccionario con la estructura anidada del DataFrame.
        """
        if df.empty:
            return {}
        return df.to_dict(orient='records')

    # ...existing code...

    @staticmethod
    def expand_comma_separated_column(df: pd.DataFrame, column_to_expand: str) -> pd.DataFrame:
        """
        Expande una columna que contiene valores separados por comas O listas en filas separadas.
        
        Args:
            df (pd.DataFrame): DataFrame original
            column_to_expand (str): Nombre de la columna que contiene valores separados por comas o listas
            
        Returns:
            pd.DataFrame: DataFrame expandido con una fila por cada valor separado por coma o elemento de lista
        """
        if df.empty or column_to_expand not in df.columns:
            return df
        
        expanded_rows = []
        
        for _, row in df.iterrows():
            comma_separated_value = row[column_to_expand]
            
            if isinstance(comma_separated_value, (list, tuple)):
                # Si es una lista, iterar directamente sobre sus elementos
                for value in comma_separated_value:
                    if value and str(value).strip():  # Solo añadir si el valor no está vacío
                        new_row = row.to_dict().copy()
                        new_row[column_to_expand] = str(value).strip()
                        expanded_rows.append(new_row)
                continue
            
            # Si el valor es NaN, None o vacío, mantener la fila original
            if pd.isna(comma_separated_value) or not str(comma_separated_value).strip():
                expanded_rows.append(row.to_dict())
                continue
            
            # Dividir por comas y crear una fila por cada valor (comportamiento original)
            values = [value.strip() for value in str(comma_separated_value).split(',')]
            
            for value in values:
                if value:  # Solo añadir si el valor no está vacío
                    new_row = row.to_dict().copy()
                    new_row[column_to_expand] = value
                    expanded_rows.append(new_row)
        
        return pd.DataFrame(expanded_rows) if expanded_rows else df