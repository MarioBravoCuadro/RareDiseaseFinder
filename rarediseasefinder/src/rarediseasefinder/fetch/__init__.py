# from .pharos_fetch import *
# from .selleckchem_fetch import *
from .uniprot_fetch import *

# from .pharos_fetch import __all__ as pharos_all
# from .selleckchem_fetch import __all__ as selleckchem_all
from .uniprot_fetch import __all__ as uniprot_all

# Definir qué se exporta con import *
__all__ = [
    # *pharos_all,
    # *selleckchem_all,
    *uniprot_all,
]