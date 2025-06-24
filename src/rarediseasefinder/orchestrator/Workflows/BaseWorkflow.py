from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd

from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow
from src.rarediseasefinder.orchestrator.WorkflowSteps.BaseWorkflowStep import BaseWorkflowStep
from src.rarediseasefinder.core.BaseFilter import BaseFilter
from src.rarediseasefinder.orchestrator.Workflows.ResultFormatter import ResultFormatter


class BaseWorkflow(IWorkflow, ABC):
    """
    Clase base para implementar workflows que siguen el patrón de tres etapas.
    Proporciona la infraestructura básica para ejecutar pasos con dependencias.
    """

    def __init__(self, name: str = None, description: str = None):
        """
        Inicializa el workflow con sus propiedades básicas.
        
        Args:
            name (str, optional): Nombre del workflow. Por defecto usa el nombre de la clase.
            description (str, optional): Descripción del workflow.
        """
        self._workflow_state = "stage_1"  # Estado inicial siempre es stage_1
        self._search_param = ""
        self._name = name or self.__class__.__name__
        self._description = description or f"Workflow {self._name}"
        self._listOfSteps = []
        self._minium_methods_by_step = {}
        self._optional_methods_by_step = {}
        self._step_params = {}  # Almacena los parámetros resueltos para cada step
        
        # Inicialización del workflow
        self._initialize_steps()
        self._configure_minimum_methods()
        self._optional_methods_by_step = self.generate_optional_methods()
        
        # Iniciar en stage_1
        self.stage_1_pipeline()

    # ---- Implementación de propiedades requeridas por IWorkflow ----
    
    @property
    def workflow_state(self) -> str:
        return self._workflow_state

    @workflow_state.setter
    def workflow_state(self, value: str) -> None:
        self._workflow_state = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def listOfSteps(self) -> List:
        return self._listOfSteps

    @listOfSteps.setter
    def listOfSteps(self, value: List) -> None:
        self._listOfSteps = value

    @property
    def search_param(self) -> str:
        return self._search_param

    @search_param.setter
    def search_param(self, value: str) -> None:
        self._search_param = value

    @property
    def minium_methods_by_step(self) -> Dict:
        return self._minium_methods_by_step

    @minium_methods_by_step.setter
    def minium_methods_by_step(self, value: Dict) -> None:
        self._minium_methods_by_step = value

    @property
    def optional_methods_by_step(self) -> Dict:
        return self._optional_methods_by_step

    @optional_methods_by_step.setter
    def optional_methods_by_step(self, value: Dict) -> None:
        self._optional_methods_by_step = value

    # ---- Métodos abstractos que deben implementar las clases derivadas ----
    
    @abstractmethod
    def _initialize_steps(self) -> None:
        """
        Inicializa los steps específicos de cada workflow.
        Cada workflow debe implementar este método para definir sus steps.
        """
        pass

    @abstractmethod
    def _configure_minimum_methods(self) -> None:
        """
        Configura los métodos mínimos requeridos para cada step.
        Cada workflow debe implementar este método para definir su configuración específica.
        """
        pass
        
    @abstractmethod
    def _get_execution_order(self) -> List[str]:
        """
        Define el orden de ejecución de los steps para este workflow.
        Este orden debe respetar las dependencias entre steps.
        
        Returns:
            List[str]: Lista de nombres de steps en orden de ejecución
        """
        pass
        
    @abstractmethod
    def _resolve_search_params(self) -> None:
        """
        Resuelve los parámetros de búsqueda para todos los steps del workflow
        basándose en el parámetro de búsqueda inicial y las dependencias entre steps.
        
        Este método debe modificar el diccionario self._step_params.
        """
        pass
        
    @abstractmethod
    def _get_category_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Define la configuración de categorías para este workflow.
        
        Returns:
            Dict[str, Dict[str, Any]]: Configuración de categorías
        """
        pass

    @abstractmethod
    def _get_method_category_mapping(self) -> Dict[str, str]:
        """
        Define el mapeo entre métodos y categorías.
        
        Returns:
            Dict[str, str]: Mapeo de "method_id" a "category_id"
        """
        pass

    # ---- Métodos de inicialización y configuración de steps ----
    
    def add_step_to_list_of_steps(self, step: Dict[str, Any]) -> None:
        """
        Añade un step a la lista de steps del workflow.
        
        Args:
            step (Dict[str, Any]): Diccionario con nombre del step como clave y la clase del step como valor.
        """
        self._listOfSteps.append(step)

    def instantiate_steps(self) -> None:
        """
        Instancia todos los steps añadidos a la lista de steps.
        """
        for step in self._listOfSteps:
            for step_name, step_class in step.items():
                # Reemplaza el diccionario por la instancia del step
                step[step_name] = step_class()

    def get_step(self, step_name: str) -> Optional[BaseWorkflowStep]:
        """
        Obtiene un step por su nombre.
        
        Args:
            step_name (str): Nombre del step a buscar.
            
        Returns:
            Optional[BaseWorkflowStep]: Instancia del step o None si no se encuentra.
        """
        for step in self._listOfSteps:
            for name, instance in step.items():
                if name == step_name:
                    return instance
        return None

    def generate_optional_methods(self) -> Dict[str, Any]:
        """
        Genera los métodos opcionales para cada step basándose en los métodos mínimos.
        Por defecto, devuelve un diccionario vacío que puede ser sobrescrito en clases derivadas.
        
        Returns:
            Dict[str, Any]: Diccionario con métodos opcionales por step.
        """
        return {}
        
    def _find_step_config(self, step_name: str) -> Optional[Dict[str, Any]]:
        """
        Encuentra la configuración para un step específico.
        
        Args:
            step_name (str): Nombre del step a buscar
            
        Returns:
            Optional[Dict[str, Any]]: Configuración del step o None si no se encuentra
        """
        for step_key, config in self._minium_methods_by_step.items():
            if config.get("step_name") == step_name:
                return config
        return None

    # ---- Implementación de las tres etapas del workflow ----
    
    def stage_1_pipeline(self) -> None:
        """
        Configura el workflow para la etapa 1.
        Esta implementación establece el estado a stage_1.
        """
        self.workflow_state = "stage_1"

    def stage_2_pipeline(self) -> None:
        """
        Configura el workflow para la etapa 2.
        Esta implementación establece el estado a stage_2.
        """
        self.workflow_state = "stage_2"

    def stage_3_pipeline(self) -> Dict[str, Any]:
        """
        Ejecuta el pipeline principal del workflow en la etapa 3.
        
        Returns:
            Dict[str, Any]: Estructura JSON con categorías y resultados.
            
        Raises:
            ValueError: Si el parámetro de búsqueda está vacío.
        """
        # Verificar precondiciones
        if not self._search_param:
            raise ValueError("El parámetro de búsqueda no puede estar vacío. Utiliza set_search_param primero.")
        
        # Limpiar parámetros de búsqueda anteriores
        self._step_params = {}
        
        # Resolver parámetros de búsqueda para todos los steps
        self._resolve_search_params()
        
        # Obtener el orden de ejecución para este workflow
        execution_order = self._get_execution_order()
        
        # Resultados finales para formateo
        final_results = []
        
        # Ejecutar steps en el orden determinado
        for step_name in execution_order:
            # Buscar la configuración de este step
            step_config = self._find_step_config(step_name)
            if not step_config:
                print(f"Warning: No hay configuración para '{step_name}', saltando.")
                continue
                
            # Obtener el step
            step = self.get_step(step_name)
            if not step:
                print(f"Warning: Step '{step_name}' no encontrado, saltando.")
                continue
                
            # Verificar si tenemos un parámetro de búsqueda para este step
            search_param = self._step_params.get(step_name)
            
            # Si no hay parámetro disponible, saltar este step
            if search_param is None:
                print(f"Warning: No se resolvió el parámetro de búsqueda para '{step_name}', saltando.")
                continue
            
            # Configurar los filtros
            processor_name = step_config.get("processor")
            methods = step_config.get("methods", [])
            
            try:
                # Crear y configurar filtros
                filters = BaseFilter(methods, processor_name)
                filters.add_client_search_params(search_param)
                
                # Aplicar filtros al step
                step.set_filters(filters)
                
                # Procesar el step
                result_dict = step.process()
                
                # Almacenar los resultados para formateo final
                for method in methods:
                    method_id = method.get("METHOD_ID")
                    if method_id in result_dict:
                        final_results.append((step_name, result_dict[method_id], method_id))
                
            except Exception as e:
                print(f"Error procesando step {step_name}: {str(e)}")
        
        # Formatear resultados
        formatted_results = self._format_results(final_results)
        
        # Volver a stage_1
        self.workflow_state = "stage_1"
        
        return formatted_results

    def _format_results(self, results: List[tuple]) -> Dict[str, Any]:
        """
        Formatea los resultados del workflow usando el formateador especializado.
        
        Args:
            results (List[tuple]): Lista de tuplas con (nombre_step, resultado, method_id).
            
        Returns:
            Dict[str, Any]: Estructura JSON con categorías, subcategorías y contenidos.
        """
        category_config = self._get_category_config()
        method_category_mapping = self._get_method_category_mapping()
        grouping_config = self._get_grouping_config()
        
        return ResultFormatter.format_workflow_results(
            results, 
            category_config, 
            method_category_mapping,
            grouping_config
        )
        
    def _get_grouping_config(self) -> Dict[str, Optional[str]]:
        """
        Define qué métodos requieren agrupación de sus DataFrames y por qué columna.
        Puede ser sobrescrito por las clases derivadas.
        
        Returns:
            Dict[str, Optional[str]]: Mapeo de method_id a columna de agrupación
        """
        # Por defecto, no se agrupa ningún dataframe
        return {}

    # ---- Métodos para manipular el workflow desde IWorkflow ----
    
    def set_filter_to_method(self, filters: Dict[str, Any], workflow_step_name: str, workflow_step_method_name: str) -> None:
        """
        Establece filtros para un método específico en un step.
        
        Args:
            filters (Dict[str, Any]): Filtros a establecer.
            workflow_step_name (str): Nombre del step.
            workflow_step_method_name (str): Nombre del método.
            
        Raises:
            ValueError: Si el workflow no está en la etapa correcta o si el step/método no existe.
        """
        # Verificar que estamos en la etapa correcta
        if self._workflow_state != "stage_2":
            raise ValueError(f"Operación 'set_filter_to_method' no permitida. Workflow está en stage '{self._workflow_state}' pero se requiere stage 'stage_2'")
        
        # Buscar el step y actualizar sus filtros
        step = self.get_step(workflow_step_name)
        if not step:
            raise ValueError(f"Step '{workflow_step_name}' no encontrado")
        
        # Obtener el filtro actual y actualizarlo
        step_filters = step.get_filters()
        if not step_filters:
            raise ValueError(f"El step '{workflow_step_name}' no tiene filtros configurados")
        
        step_filters.set_filter_to_method(filters, workflow_step_method_name)

    def set_search_param(self, search_param: str) -> None:
        """
        Establece el parámetro de búsqueda para el workflow.
        
        Args:
            search_param (str): Parámetro de búsqueda.
            
        Raises:
            ValueError: Si el workflow no está en la etapa correcta.
        """
        # Verificar que estamos en la etapa correcta
        if self._workflow_state != "stage_2":
            raise ValueError(f"Operación 'set_search_param' no permitida. Workflow está en stage '{self._workflow_state}' pero se requiere stage 'stage_2'")
        
        self._search_param = search_param

    def set_stage_2(self) -> None:
        """
        Cambia el workflow a la etapa 2.
        
        Raises:
            ValueError: Si el workflow no está en la etapa 1.
        """
        if self._workflow_state != "stage_1":
            raise ValueError(f"Operación 'set_stage_2' no permitida. Workflow está en stage '{self._workflow_state}' pero se requiere stage 'stage_1'")
        
        self.stage_2_pipeline()

    def set_stage_3(self) -> None:
        """
        Cambia el workflow a la etapa 3.
        
        Raises:
            ValueError: Si el workflow no está en la etapa 2.
        """
        if self._workflow_state != "stage_2":
            raise ValueError(f"Operación 'set_stage_3' no permitida. Workflow está en stage '{self._workflow_state}' pero se requiere stage 'stage_2'")
        
        self.workflow_state = "stage_3"

    def steps_execution(self) -> Dict[str, Any]:
        """
        Ejecuta el workflow completo.
        
        Returns:
            Dict[str, Any]: Resultados del workflow.
            
        Raises:
            ValueError: Si el workflow no está en la etapa 3.
        """
        if self._workflow_state != "stage_3":
            raise ValueError(f"Operación 'steps_execution' no permitida. Workflow está en stage '{self._workflow_state}' pero se requiere stage 'stage_3'")
        
        return self.stage_3_pipeline()