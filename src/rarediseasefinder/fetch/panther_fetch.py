import requests

def obtener_panther_class(gene_id):
    """
    Obtiene la clase PANTHER de un gen dado su ID. También funciona con el symbol.

    Args:
        gene_id (str): El ID del gen.

    Returns:
        str: La clase PANTHER del gen.
    """
    url = f"https://pantherdb.org/services/oai/pantherdb/geneinfo?geneInputList={gene_id}&organism=9606"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            annotations = data['search']['mapped_genes']['gene']['annotation_type_list']['annotation_data_type']

            if len(annotations) > 1:
                # Obtener el nombre de la annotation en la posición 1
                annotation_name = annotations[1]['annotation_list']['annotation']['name']
                return annotation_name
            else:
                return "Panther class no encontrada o no disponible."
        except KeyError as e:
            return f"Error al acceder a la clave: {e}"
    else:
        return f"PantherDB no disponible. Error: {response.status_code}"

__all__ = ["obtener_panther_class"]