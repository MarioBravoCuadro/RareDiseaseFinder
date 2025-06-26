import json
from typing import Dict, List, Any, Union

class JSONFactory:
    """
    Clase para generar una estructura JSON estandarizada para los resultados de RareDiseaseFinder.
    Permite especificar directamente sección, título, tipo de display y datos.
    """
    
    def __init__(self):
        """
        Inicializa la estructura básica del JSON con las categorías predefinidas.
        """
        # Definir las secciones principales del documento
        self.sections = [
            "DESCRIPCIÓN",
            "PROCESOS (Funcionoma)",
            "PATHWAYS",
            "INTERACCIONES",
            "ENFERMEDADES",
            "TERAPÉUTICA",
            "REFERENCIAS"
        ]
        
        # Inicializar estructura JSON
        self.json_structure = {
            "categories": [
                {"section": section, "content": []} for section in self.sections
            ]
        }
    
    def add_content(self, section: str, title: str, display: str, data: Any) -> bool:
        """
        Añade contenido a una sección específica.
        
        Args:
            section (str): Nombre de la sección (debe coincidir con una de las predefinidas)
            title (str): Título del contenido
            display (str): Tipo de visualización ('table', 'chart', etc.)
            data (Any): Datos a mostrar (ya procesados por dataframe_todict u otra función)
            
        Returns:
            bool: True si se añadió correctamente, False si la sección no existe
        """
        # Buscar la sección
        for category in self.json_structure["categories"]:
            if category["section"] == section:
                # Añadir el contenido
                content_item = {
                    "title": title,
                    "display": display,
                    "data": data
                }
                category["content"].append(content_item)
                return True
        
        # Si no se encontró la sección
        return False
    
    def get_json(self) -> Dict:
        """
        Devuelve la estructura JSON completa.
        
        Returns:
            Dict: La estructura JSON construida
        """
        return self.json_structure
    
    def get_json_string(self, indent: int = 2) -> str:
        """
        Devuelve la estructura JSON como cadena formateada.
        
        Args:
            indent (int): Nivel de indentación para la cadena JSON
            
        Returns:
            str: JSON formateado como cadena
        """
        return json.dumps(self.json_structure, indent=indent)
    
    def save_to_file(self, filepath: str) -> bool:
        """
        Guarda el JSON en un archivo.
        
        Args:
            filepath (str): Ruta del archivo donde guardar el JSON
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.json_structure, f, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar JSON en archivo: {str(e)}")
            return False