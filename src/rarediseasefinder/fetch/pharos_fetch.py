import pandas as pd
import requests
from rarediseasefinder.fetch.uniprot_fetch import procesar_uniprot
from rarediseasefinder.fetch.selleckchem_fetch import obtener_link_selleckchem

graphql_url = "https://pharos-api.ncats.io/graphql"

def procesar_pharos(target):

    query = f"""
        query ObtenerInfoVariante {{
        target(q: {{ sym: "{target}" }}) {{
            nombre: name
            uniprot_ID: uniprot
            descripcion: description
            claseDiana: tdl
            secuencia: seq

            referenciaOMIM: mim {{
            OMIM_ID: mimid
            nombre: term
            }}

            ligandosConocidos: ligands {{
            nombre: name
            ligando_ID: ligid
            }}

            deLosCualesSonFarmacosAprobados: ligands(isdrug: true) {{
            nombre: name
            ligando_ID: ligid
            }}

            relacionProteinaProteina: ppis{{
            target {{
                nombre: name
                proteina_ID: sym
                secuencia: seq
                claseDiana: tdl
            }}
            propiedadesRelacion: props {{
                name
                value
            }}
            }}

            numeroDeViasPorFuente: pathwayCounts {{
            fuente: name
            numVias: value
            }}

            vias: pathways {{
            viaPharos_ID: pwid
            nombre: name
            fuente: type
            fuente_ID: sourceID
            url
            }}
        }}
        }}
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()

    # Extraer los datos
    if "data" in data and "target" in data["data"]:
        dataIsfetched = True
        target_data = data["data"]["target"]

        # Crear DataFrame con información principal
        df_info = pd.DataFrame([{key: target_data[key] for key in ["nombre", "uniprot_ID", "descripcion", "claseDiana", "secuencia"]}])

        # Lista de dataframes que nos devuelve uniprot_fetch
        df_uniprot = procesar_uniprot(target_data.get("uniprot_ID", []))

        # Crear DataFrame de referencia OMIM
        df_omim = pd.DataFrame(target_data.get("referenciaOMIM", []))

        # Crear DataFrame de ligandos conocidos
        df_ligandos = pd.DataFrame(target_data.get("ligandosConocidos", []))

        df_ligandos['Selleckchem'] = df_ligandos['nombre'].apply(
        lambda x: obtener_link_selleckchem(x) or 'No encontrado'
        )

        # Crear DataFrame de fármacos aprobados
        df_farmacos = pd.DataFrame(target_data.get("deLosCualesSonFarmacosAprobados", []))

        df_farmacos['Selleckchem'] = df_farmacos['nombre'].apply(
        lambda x: obtener_link_selleckchem(x) or 'No encontrado'
        )

        # Crear DataFrame de relaciones proteína-proteína con priorización
        relaciones = []

        # Ordenar y filtrar las relaciones
        relaciones_raw = target_data.get("relacionProteinaProteina", [])

        # Definir prioridad de clases
        prioridad_clases = {
            "Tclin": 1,
            "Tchem": 2,
            "Tbio": 3,
            "Tdark": 4
        }

        # Función para ordenar
        def ordenar_por_clase(relacion):
            clase = relacion.get("target", {}).get("claseDiana", "")
            return prioridad_clases.get(clase, 5)  # 5 para clases desconocidas

        # Ordenar y tomar top 10
        relaciones_ordenadas = sorted(
            relaciones_raw,
            key=ordenar_por_clase
        )[:10]

        # Procesar solo las top 10
        for rel in relaciones_ordenadas:
            if "target" in rel and "propiedadesRelacion" in rel:
                # Filtrar propiedades por relevancia (p_wrong, p_ni, p_int, novelty)
                propiedades_filtradas = []
                for prop in rel["propiedadesRelacion"]:
                    if prop["name"] in ["p_wrong", "p_ni"]:
                    # if prop["name"] in ["p_wrong", "p_ni", "p_int", "novelty"] Para sacar los cuatro tipos
                        propiedades_filtradas.append(prop)

                # Ordenar propiedades por prioridad
                prioridad_propiedades = {
                    "p_wrong": 1,
                    "p_ni": 2
                # "p_int": 3,
                # "novelty": 4
                }
                propiedades_ordenadas = sorted(
                    propiedades_filtradas,
                    key=lambda x: prioridad_propiedades.get(x["name"], 5)
                )

                # Agregar solo las propiedades ordenadas
                for prop in propiedades_ordenadas:
                    relaciones.append({
                        "Proteina": rel["target"]["nombre"],
                        "Proteina_ID": rel["target"]["proteina_ID"],
                        "Clase Diana": rel["target"]["claseDiana"],
                        "Propiedad": prop["name"],
                        "Valor": prop["value"]
                    })

        df_relaciones = pd.DataFrame(relaciones)

        #Crear Dataframe de numeroDeViasPorFuente
        df_numero_vias_por_fuente = pd.DataFrame(target_data.get("numeroDeViasPorFuente", []))

        # Crear DataFrame de vías
        df_vias = pd.DataFrame(target_data.get("vias", []))

    else:
        dataIsfetched = False



__all__ = ['procesar_pharos']