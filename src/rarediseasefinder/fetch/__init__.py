from .pharos_fetch import procesar_pharos
from .selleckchem_fetch import obtener_link_selleckchem
from .uniprot_fetch import procesar_uniprot, procesar_uniprot_target
__all__ = [
    "procesar_pharos",
    "obtener_link_selleckchem",
    "procesar_uniprot",
    "procesar_uniprot_target"
]
