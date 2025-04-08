from IPython.display import display, Markdown

def mostrar_dataframe(titulo, df):
    """
    Muestra un DataFrame con un título en Markdown.
    
    :param titulo: Título que se mostrará antes del DataFrame.
    :param df: DataFrame que se desea mostrar.
    """
    # Mostrar el título
    display(Markdown(f"### {titulo}"))
    # Mostrar el DataFrame
    display(df)

def mostrar_dataframe_groupby(titulo, df, group_by_column):
    """
    Muestra un DataFrame agrupado por una columna específica con un título en Markdown.
    
    :param titulo: Título que se mostrará antes del DataFrame.
    :param df: DataFrame que se desea mostrar.
    :param group_by_column: Columna por la que se agrupará el DataFrame.
    """
    # Agrupar el DataFrame por la columna especificada
    grouped = df.groupby(group_by_column)
    
    # Mostrar cada grupo
    for name, group in grouped:
        mostrar_dataframe(f"{titulo}: {name}", group)
        display(Markdown("---"))
