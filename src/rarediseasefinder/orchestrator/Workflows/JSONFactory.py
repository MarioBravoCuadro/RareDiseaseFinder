import json
from typing import Dict
import datetime

class JSONFactory:
    """
    Clase para generar una estructura JSON estandarizada para los resultados de RareDiseaseFinder.
    Permite especificar directamente sección, título, tipo de display y datos.
    """
    search_term: str
    date: str

    def __init__(self,search_term: str = ""):
        """
        Inicializa la estructura básica del JSON con las categorías predefinidas.
        """
        # Definir las secciones principales del documento
        self.sections = [
            "DESCRIPCIÓN",
            "PROCESOS",
            "PATHWAYS",
            "INTERACCIONES",
            "ENFERMEDADES",
            "TERAPÉUTICA",
            "REFERENCIAS",
            "MÉTODOS OPCIONALES",
            "ENLACES EXTERNOS",
        ]
        
        # Inicializar estructura JSON
        self.json_structure = { 
            "search_term": search_term,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categories": [
                {"section": section, "content": []} for section in self.sections
            ]
        }
    
    def set_search_term(self, search_term: str) -> None:
        """
        Establece el término de búsqueda en la estructura JSON.
        
        Args:
            search_term (str): Término de búsqueda a establecer
        """
        self.json_structure["search_term"] = search_term
    
    def set_date(self) -> None:
        """
        Actualiza la fecha actual en la estructura JSON.    
        """
        self.json_structure["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_content(self, section: str, title: str, display: str, data: dict) -> bool:
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
    
    def save_to_file(self, filepath: str = None) -> bool:
        """
        Guarda el JSON en un archivo. Si no se especifica filepath, usa searchterm_fecha_hora.json en la raíz del proyecto (detectada automáticamente).
        Sobrescribe el archivo si ya existe.
        Args:
            filepath (str): Ruta del archivo donde guardar el JSON
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        import os
        from datetime import datetime
        try:
            if not filepath:
                searchterm = self.json_structure.get('search_term', 'resultado')
                fecha = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                # Detectar la raíz del proyecto automáticamente
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
                tests_dir = os.path.join(base_dir, 'tests')
                filename = f"{searchterm}_{fecha}.json"
                filepath = os.path.join(tests_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.json_structure, f, indent=2, ensure_ascii=False, default=str)
                self.delete_json()  # Reiniciar la estructura después de guardar
            print(f"\033[92mResultado guardado en: {filepath}\033[0m")
            return True
        except Exception as e:
            print(f"Error al guardar JSON en archivo: {str(e)}")
            return False
        
    def delete_json(self) -> bool:
        """
        Elimina el JSON actual, reiniciando la estructura a su estado inicial vacío.
        Mantiene las secciones predefinidas pero vacía todo el contenido.
        
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            self.json_structure = {
                "search_term": "",
                "date": "",
                "categories": [
                    {"section": section, "content": []} for section in self.sections
                ]
            }
            self.search_term = ""
            self.date = ""
            return True
            
        except Exception as e:
            print(f"❌ Error al reiniciar JSON: {str(e)}")
            return False