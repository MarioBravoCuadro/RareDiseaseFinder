from typing import Union, List, Dict, Any

import pandas as pd


class DataframesUtils:
    @staticmethod
    def group_dataframe(df: pd.DataFrame, group_column: str = None) -> List[pd.DataFrame]:
        """
        Agrupa un DataFrame por una columna específica.

        Args:
            df (pd.DataFrame): DataFrame a agrupar.
            group_column (str, optional): Columna para agrupar.

        Returns:
            List[pd.DataFrame]: Lista de DataFrames agrupados.
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
