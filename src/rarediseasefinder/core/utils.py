"""
utils.py

Este módulo contiene funciones auxiliares para determinar si el código se está ejecutando en Google Colab y para crear un directorio único para perfiles de usuario de Chrome.
"""

import os
import sys

def is_colab():
    """
    Verifica si el código se está ejecutando en Google Colab.

    Returns:
        bool: True si se está ejecutando en Google Colab, False en caso contrario.
    """
    return 'google.colab' in sys.modules

def get_unique_directory():
    """
    Crea y devuelve un directorio único para almacenar perfiles de usuario de Chrome.

    Si el código se ejecuta en Google Colab, el directorio se crea en "/content/ChromeProfileUnique".
    Si se ejecuta localmente, el directorio se crea en el directorio actual bajo el nombre "ChromeProfileUnique".

    Returns:
        str: La ruta al directorio único creado.
    """
    if is_colab():
        unique_dir = "/content/ChromeProfileUnique"
    else:
        unique_dir = os.path.join(os.getcwd(), "ChromeProfileUnique")
    os.makedirs(unique_dir, exist_ok=True)
    return unique_dir