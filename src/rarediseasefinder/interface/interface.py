from IPython.display import display, Markdown
def mostrar_dataframe(titulo, df):
      """ Muestra un DataFrame con título o un mensaje si está vacío """
      display(Markdown(f"## {titulo}"))
      if df.empty:
          display(Markdown("> ⚠️ No se han encontrado datos."))
      else:
          display(Markdown(df.to_markdown(index=False)))