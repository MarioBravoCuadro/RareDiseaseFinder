import os
import sys

def is_colab():
    return 'google.colab' in sys.modules

def get_unique_directory():
    if is_colab():
        unique_dir = "/content/ChromeProfileUnique"
    else:
        unique_dir = os.path.join(os.getcwd(), "ChromeProfileUnique")
    os.makedirs(unique_dir, exist_ok=True)
    return unique_dir