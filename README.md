# RareDiseaseFinder

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Descripción

RareDiseaseFinder es un sistema de búsqueda de información sobre enfermedades raras que funciona como el **backend** de un sistema más amplio. Este sistema permite realizar búsquedas exhaustivas de información biomédica a través de múltiples fuentes de datos especializadas, proporcionando resultados integrados y estructurados.

### 🎥 Demo del Sistema
**Frontend en funcionamiento**: https://youtu.be/ESQv-lsty60

### Arquitectura del Sistema

Este backend está diseñado para trabajar en conjunto con un frontend desarrollado en React que se encuentra en el repositorio: https://github.com/jennygatv/front-RD/

El sistema utiliza una arquitectura basada en **workflows** que permiten:
- Acceso a múltiples fuentes de datos biomédicas
- Procesamiento y normalización de información
- Filtrado y personalización de resultados
- Integración de datos de diferentes proveedores

## Estructura del Proyecto

```
RareDiseaseFinder/
├── src/
│   └── rarediseasefinder/
│       ├── core/                    # Elementos comunes del proyecto
│       │   ├── constants/           # Constantes del sistema
│       │   ├── error_handling/      # Manejo de errores
│       │   └── abstractions/        # Clases base y abstracciones
│       ├── orchestrator/            # Orquestador principal
│       │   ├── server.py           # Servidor Flask principal
│       │   └── ...                 # Lógica de orquestación
│       ├── datasources/            # Implementaciones de fuentes de datos
│       │   ├── uniprot/            # Procesador UniProt
│       │   ├── opentargets/        # Procesador OpenTargets
│       │   ├── pharos/             # Procesador Pharos
│       │   └── ...                 # Otras fuentes
│       └── main.py                 # Tests y validaciones
├── tests/                          # JSONs de prueba generados
├── docs/                          # Documentación del proyecto
├── pyproject.toml                 # Configuración de Poetry
└── README.md                      # Este archivo
```

## Fuentes de Datos Soportadas

El sistema integra las siguientes fuentes de datos biomédicas:

### Fuentes Principales
- **UniProt**: Información sobre proteínas, funciones, localizaciones subcelulares
- **OpenTargets**: Información sobre targets, enfermedades asociadas, medicamentos
- **Pharos**: Datos sobre targets farmacológicos y ligandos
- **Ensembl**: Identificadores de genes y datos genómicos
- **StringDB**: Interacciones proteína-proteína
- **PantherDB**: Clasificaciones funcionales y pathways
- **PharmGKB**: Información farmacogenómica
- **DrugCentral**: Información sobre fármacos

### Fuentes Complementarias
- **SelleckChem**: Enlaces a información de compuestos
- **GuideToPharmacology**: Información farmacológica
- **PPIAtlas**: Atlas de interacciones proteína-proteína

## Requisitos del Sistema

### Requisitos de Software
- **Python**: 3.9 o superior
- **Poetry**: Para gestión de dependencias
- **Navegador web**: Para acceder al frontend

### Dependencias Principales
- Flask 3.1.1
- Pandas 2.0.0+
- Requests 2.31.0+
- BeautifulSoup4 4.12.2+
- Selenium 4.9.0+

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/MarioBravoCuadro/RareDiseaseFinder.git
cd RareDiseaseFinder
```

### 2. Instalar Poetry
Si no tienes Poetry instalado, instálalo siguiendo las instrucciones oficiales:

**En Linux/macOS:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**En Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 3. Configurar el Proyecto con Poetry
```bash
# Instalar todas las dependencias
poetry install

# Activar el entorno virtual
poetry shell
```

### 4. Verificar la Instalación
```bash
# Ejecutar los tests para verificar que todo funciona correctamente
cd src/rarediseasefinder
python main.py
```

## Ejecución del Sistema

### Ejecutar el Backend
Para iniciar el servidor backend, navega al directorio del orquestador y ejecuta:

```bash
cd src/rarediseasefinder/orchestrator
flask --app server.py run --host=0.0.0.0 --port=4999
```

El servidor estará disponible en: `http://localhost:4999`

### Ejecutar con el Frontend
Para una experiencia completa, también ejecuta el frontend:

1. Clona el repositorio del frontend:
```bash
git clone https://github.com/jennygatv/front-RD/
```

2. Sigue las instrucciones de instalación del frontend

3. Ejecuta ambos sistemas simultáneamente para ver el funcionamiento completo

## API REST

El sistema expone una API REST organizada en tres stages:

### Stage 1: Obtención de Información (GET)
- `/stage1/get_workflows` - Obtener lista de workflows disponibles
- `/stage1/get_sources` - Obtener fuentes de un workflow específico
- `/stage1/get_methods` - Obtener métodos de una fuente específica
- `/stage1/get_filters` - Obtener filtros de un método específico

### Stage 2: Configuración (POST)
- `/stage2/set_optional_method` - Modificar métodos opcionales
- `/stage2/set_filter` - Modificar filtros específicos
- `/stage2/set_search_param` - Establecer parámetro de búsqueda

### Stage 3: Ejecución (POST)
- `/stage3/start_workflow` - Ejecutar workflow y obtener resultados

### Documentación Interactiva

La documentación completa de todos los endpoints está disponible a través de Swagger UI cuando el servidor está ejecutándose:

```
http://localhost:4999/docs
```

Esta interfaz interactiva permite:
- Explorar todos los endpoints disponibles
- Ver parámetros requeridos y opcionales
- Probar las llamadas a la API directamente desde el navegador
- Consultar ejemplos de request/response para cada endpoint

## Workflows Disponibles

El sistema ofrece varios workflows predefinidos:

- **FULL WORKFLOW**: Incluye todas las secciones de información
- **NO PHAROS WORKFLOW**: Incluye todas las secciones de información sin acceder a la fuente de datos Pharos
- **NO PANTHER WORKFLOW**: Incluye todas las secciones de información sin acceder a la fuente de datos PantherDB


## Testing

### Ejecutar Tests
Los tests principales se encuentran en:
```bash
cd src/rarediseasefinder
python main.py
```

Este archivo prueba el correcto funcionamiento de todos los procesadores de fuentes de datos.

### Resultados de Tests
Los resultados de los tests se almacenan en la carpeta `tests/` como archivos JSON. Estos JSONs representan la estructura de datos que se envía al frontend.

## Desarrollo y Contribución

### Arquitectura del Código

El sistema utiliza el patrón **Retriever/Parser/Filter/Processor** para mantener un código limpio y modular:

- **Retriever**: Obtiene datos de fuentes externas
- **Parser**: Normaliza y estructura los datos
- **Filter**: Gestiona filtros específicos
- **Processor**: Coordina el flujo de datos

### Añadir Nuevas Fuentes de Datos

Para implementar una nueva fuente de datos:

1. Consulta la documentación en `/docs/` (especialmente la guía de implementación de proveedores)
2. Implementa las clases requeridas:
   - `YourSourceClient` (hereda de `BaseClient`)
   - `YourSourceParser` (hereda de `BaseParser`)
   - `YourSourceProcessor` (hereda de `BaseProcessor`)
3. Integra la fuente en el sistema de workflows

### Estructura de Clases

```python
# Ejemplo de implementación
class YourSourceClient(BaseClient):
    def _ping_logic(self):
        # Implementar lógica de conexión
        pass

class YourSourceParser(BaseParser):
    def parse_your_data(self, raw_data):
        # Implementar parseo específico
        pass

class YourSourceProcessor(BaseProcessor):
    def get_method_map(self):
        # Mapear métodos disponibles
        pass
```

## Limitaciones y Consideraciones

### Limitaciones Actuales
- No requiere autenticación con APIs externas en esta versión
- No utiliza base de datos (procesamiento en memoria)
- Dependiente de la disponibilidad de fuentes externas

### Recomendaciones de Uso
- **Ejecutar backend y frontend simultáneamente** para experimentar la funcionalidad completa
- Verificar conectividad a internet para acceso a fuentes externas
- Revisar logs del servidor para diagnosticar problemas

## Documentación Adicional

La documentación detallada está disponible en la carpeta `/docs/`:
- Guía de desarrollador para integración con API REST
- Guía de implementación de nuevos proveedores de datos
- Inventario de extracción de información de fuentes

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

**Autor**: Mario Bravo Cuadro  
**Email**: mario.bravo.cuadro@alumnos.upm.es  

**Autor**: Emil Stelian Pintilie 
**Email**: emil.pintilie@alumnos.upm.es  

## Enlaces Relacionados

- **Frontend**: https://github.com/jennygatv/front-RD/
- **Documentación de Poetry**: https://python-poetry.org/docs/
- **Documentación de Flask**: https://flask.palletsprojects.com/

---

> **Nota**: Este README proporciona una guía completa para desarrolladores. Para obtener información más detallada sobre la implementación de nuevas fuentes de datos, consulta la documentación en la carpeta `/docs/`.
