import fetch.uniprot_fetch
from interface import mostrar_dataframe, mostrar_dataframe_groupby

print("PRUEBA DE FETCH UNIPROT:")
# Obtener los DataFrames a partir del ID de UniProt
dataframes = fetch.uniprot_fetch.procesar_uniprot("P02766")

# Mostrar DataFrames completos
mostrar_dataframe("1. Función", dataframes["Function"])
mostrar_dataframe("2. Localización Subcelular", dataframes["Subcellular Location"])
mostrar_dataframe_groupby("3. Enfermedades", dataframes["Disease"], "Nombre")  # Agrupar por "Nombre"
mostrar_dataframe("4. Variantes", dataframes["Variants"])
mostrar_dataframe("5. Interacciones", dataframes["Interactions"])
