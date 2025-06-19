import enum
import json
import uuid
import logging
from datetime import datetime, timezone

from IPython.core.magic_arguments import argument
from flask import url_for, Flask, abort, request
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import fields, Schema
from narwhals import Boolean

from src.rarediseasefinder.orchestrator.Orchestrator import Orchestrator
from src.rarediseasefinder.orchestrator.Workflows.Workflow import Workflow
from src.rarediseasefinder.orchestrator.api import workflows

server = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Schemas para todas las respuestas
class WorkflowSchema(Schema):
    name = fields.Str(required=True)
    status = fields.Bool(required=True)

class WorkflowListSchema(Schema):
    class Meta:
        description = "Lista de workflows disponibles"
    workflows = fields.List(fields.Nested(WorkflowSchema), required=True)

class StepsAvailableSchema(Schema):
    are_steps_avaliable = fields.Bool(required=True)

class ListOfStepsSchema(Schema):
    steps = fields.List(fields.Dict(), required=True)

class MethodSchema(Schema):
    METHOD_ID = fields.Str(required=True)
    METHOD_PARSER_FILTERS = fields.Dict(required=True)

class StepMethodSchema(Schema):
    step_name = fields.Str(required=True)
    processor = fields.Str(required=True)
    methods = fields.List(fields.Nested(MethodSchema), required=True)

class MinimumMethodsListSchema(Schema):
    class Meta:
        description = "Lista de métodos mínimos requeridos"
    minimum_methods = fields.List(fields.Nested(StepMethodSchema), required=True)

class OptionalMethodsListSchema(Schema):
    class Meta:
        description = "Lista de métodos opcionales"
    optional_methods = fields.List(fields.Nested(StepMethodSchema), required=True)

class MethodsFiltersSchema(Schema):
    class Meta:
        description = "Filtros de métodos configurados"
    filters = fields.Dict(required=True)

class SetStage2Schema(Schema):
    class Meta:
        description = "Setea el stage 2 en el orquestrador"

class SelectedOptionalMethodSchema(Schema):
    class Meta:
        description = "Método opcional seleccionado aplicado"

class FilterAppliedSchema(Schema):
    class Meta:
        description = "Filtro aplicado al método"

class SearchParamSetSchema(Schema):
    class Meta:
        description = "Parámetro de búsqueda establecido"

class SetStage3Schema(Schema):
    class Meta:
        description = "Setea el stage 3 en el orquestrador"

class WorkflowStartedSchema(Schema):
    class Meta:
        description = "Ejecuta el workflow y devuelve el informe en formato JSON"
        unknown = "INCLUDE"  # Incluye campos desconocidos
class SetStage1Schema(Schema):
    class Meta:
        description = "Resetea el workflow al stage 1"

# Schemas para parámetros de entrada
class WorkflowNameQuerySchema(Schema):
    workflow_name = fields.Str(required=True)

class WorkflowStepNameQuerySchema(Schema):
    workflow_step_name= fields.Str(required=True)

class WorkflowStepMethodNameQuerySchema(Schema):
    workflow_step_method_name= fields.Str(required=True)

# Schemas para request body stage_2
class SelectedOptionalMethodRequestSchema(Schema):
    selected_optional_method = fields.Str(required=True)

class FilterRequestSchema(Schema):
    filters = fields.Dict(required=True)

class SearchParamRequestSchema(Schema):
    search_id = fields.Str(required=True)


class APIConfig:
    API_TITLE = "RareDiseaseFinder_API"
    API_VERSION = "V1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

server.config.from_object(APIConfig)
api = Api(server)

stage_1 = Blueprint("stage1", "__name__", url_prefix="/stage1",description="Get workflows info API")
stage_2 = Blueprint("stage2", "__name__", url_prefix="/stage2",description="Set workflows params API")
stage_3 = Blueprint("stage3", "__name__", url_prefix="/stage3",description="Process workflow API")


@stage_1.route("/get_workflows")
class TodoCollection(MethodView):
    @stage_1.response(status_code=200, schema=WorkflowListSchema)
    def get(self):
        """Obtiene la lista de workflows disponibles"""
        logger.info("GET /stage1/get_workflows - Solicitando lista de workflows")
        try:
            workflows_data = orchestrator.get_workflows()
            logger.info(f"GET /stage1/get_workflows - Encontrados {len(workflows_data)} workflows")
            return {"workflows": workflows_data}
        except Exception as e:
            logger.error(f"GET /stage1/get_workflows - Error: {str(e)}")
            abort(500, description=str(e))

@stage_1.route("/steps_available")
class StepsAvailableCollection(MethodView):
    @stage_1.arguments(WorkflowNameQuerySchema, location="query")
    @stage_1.response(status_code=200, schema=StepsAvailableSchema)
    def get(self, query_args):
        """Verifica si todos los pasos están disponibles"""
        workflow_name = query_args["workflow_name"]
        logger.info(f"GET /stage1/steps_available - Verificando disponibilidad de steps para workflow: {workflow_name}")
        try:
            workflows_data = orchestrator.get_if_all_steps_available(workflow_name)
            logger.info(f"GET /stage1/steps_available - Workflow {workflow_name} - Steps disponibles: {workflows_data}")
            return {"are_steps_avaliable": workflows_data}
        except Exception as e:
            logger.error(f"GET /stage1/steps_available - Error para workflow {workflow_name}: {str(e)}")
            abort(500, description=str(e))

@stage_1.route("/list_steps")
class ListOfStepsCollection(MethodView):
    @stage_1.arguments(WorkflowNameQuerySchema, location="query")
    @stage_1.response(status_code=200, schema=ListOfStepsSchema)
    def get(self, query_args):
        """Obtiene la lista de nombres de steps del workflow"""
        workflow_name = query_args["workflow_name"]
        logger.info(f"GET /stage1/list_steps - Solicitando lista de steps para workflow: {workflow_name}")
        try:
            workflows_data = orchestrator.get_list_of_steps_names(workflow_name)
            logger.info(f"GET /stage1/list_steps - Workflow {workflow_name} tiene {len(workflows_data) if isinstance(workflows_data, list) else 'N/A'} steps")
            return {"steps": workflows_data}
        except Exception as e:
            logger.error(f"GET /stage1/list_steps - Error para workflow {workflow_name}: {str(e)}")
            abort(500, description=str(e))

@stage_1.route("/minimum_methods")
class MinimumMethodsCollection(MethodView):
    @stage_1.arguments(WorkflowNameQuerySchema, location="query")
    @stage_1.arguments(WorkflowStepNameQuerySchema, location="query")
    @stage_1.response(status_code=200, schema=MinimumMethodsListSchema)
    def get(self,workflow_args,step_args):
        """Obtiene la lista de métodos mínimos"""
        workflow_name = workflow_args["workflow_name"]
        workflow_step = step_args["workflow_step_name"]
        logger.info(f"GET /stage1/minimum_methods - Solicitando métodos mínimos para step: {workflow_step} en workflow: {workflow_name}")
        try:
            methods_data = orchestrator.get_minium_methods_for_step_from_workflow(workflow_step,workflow_name)
            logger.info(f"GET /stage1/minimum_methods - Encontrados métodos mínimos para {workflow_step}: {methods_data}")
            print(methods_data)
            return {"minimum_methods":[methods_data]}
        except Exception as e:
            logger.error(f"GET /stage1/minimum_methods - Error para step {workflow_step} en workflow {workflow_name}: {str(e)}")
            abort(500, description=str(e))

@stage_1.route("/optional_methods")
class OptionalMethodsCollection(MethodView):
    @stage_1.arguments(WorkflowNameQuerySchema, location="query")
    @stage_1.arguments(WorkflowStepNameQuerySchema, location="query")
    @stage_1.response(status_code=200, schema=OptionalMethodsListSchema)
    def get(self,workflow_args,step_args):
        """Obtiene la lista de métodos OPCIONALES"""
        workflow_name = workflow_args["workflow_name"]
        workflow_step = step_args["workflow_step_name"]
        logger.info(f"GET /stage1/optional_methods - Solicitando métodos opcionales para step: {workflow_step} en workflow: {workflow_name}")
        try:
            methods_data = orchestrator.get_optional_methods_from_workflow(workflow_step,workflow_name)
            logger.info(f"GET /stage1/optional_methods - Encontrados métodos opcionales para {workflow_step}: {methods_data}")
            print(methods_data)
            return {"optional_methods": [methods_data]}
        except Exception as e:
            logger.error(f"GET /stage1/optional_methods - Error para step {workflow_step} en workflow {workflow_name}: {str(e)}")
            abort(500, description=str(e))

@stage_1.route("/methods_filters")
class MethodsFiltersCollection(MethodView):
    @stage_1.arguments(WorkflowNameQuerySchema, location="query")
    @stage_1.arguments(WorkflowStepNameQuerySchema, location="query")
    @stage_1.arguments(WorkflowStepMethodNameQuerySchema, location="query")
    @stage_1.response(status_code=200, schema=MethodsFiltersSchema)
    def get(self,workflow_args,step_args,workflow_step_method_name):
        """Obtiene los filtros de métodos configurados"""
        workflow_name = workflow_args["workflow_name"]
        workflow_step = step_args["workflow_step_name"]
        method_name = workflow_step_method_name["workflow_step_method_name"]
        logger.info(f"GET /stage1/methods_filters - Solicitando filtros para método: {method_name} en step: {workflow_step} workflow: {workflow_name}")
        try:
            workflow_step_method_name = workflow_step_method_name["workflow_step_method_name"]
            print(workflow_step_method_name,workflow_step,workflow_name)
            filters_data = orchestrator.get_method_filters(workflow_step_method_name,workflow_step,workflow_name)
            logger.info(f"GET /stage1/methods_filters - Filtros encontrados para {method_name}: {len(filters_data) if filters_data else 0} filtros")
            print(filters_data.values())
            return {"filters": filters_data}
        except Exception as e:
            logger.error(f"GET /stage1/methods_filters - Error para método {method_name}: {str(e)}")
            abort(500, description=str(e))

@stage_1.route("/set_stage_2")
class SetStage2(MethodView):
    @stage_1.arguments(WorkflowNameQuerySchema, location="query")
    @stage_1.response(status_code=200, schema=SetStage2Schema)
    def post(self,workflow_args):
        """Setea el workflow al stage 2"""
        workflow_name = workflow_args["workflow_name"]
        logger.info(f"GET /stage1/set_stage_2 - Cambiando workflow {workflow_name} a stage 2")
        try:
            orchestrator.set_stage_2(workflow_name)
            logger.info(f"GET /stage1/set_stage_2 - Workflow {workflow_name} cambiado exitosamente a stage 2")
            return {f"{workflow_name} set to stage_2"}
        except Exception as e:
            logger.error(f"GET /stage1/set_stage_2 - Error al cambiar workflow {workflow_name} a stage 2: {str(e)}")
            abort(500, description=str(e))

# Stage 2 endpoints
@stage_2.route("/set_optional_method")
class SetOptionalMethodCollection(MethodView):
    @stage_2.arguments(WorkflowNameQuerySchema, location="query")
    @stage_2.arguments(WorkflowStepNameQuerySchema, location="query")
    @stage_2.arguments(SelectedOptionalMethodRequestSchema, location="json")
    @stage_2.response(status_code=200, schema=SelectedOptionalMethodSchema)
    def post(self, workflow_args, step_args, json_data):
        """Establece un método opcional seleccionado"""
        workflow_name = workflow_args["workflow_name"]
        workflow_step = step_args["workflow_step_name"]
        selected_method = json_data["selected_optional_method"]
        logger.info(f"POST /stage2/set_optional_method - Estableciendo método opcional {selected_method} para step {workflow_step} en workflow {workflow_name}")
        try:
            orchestrator.set_selected_optional_method(selected_method, workflow_step, workflow_name)
            logger.info(f"POST /stage2/set_optional_method - Método opcional {selected_method} establecido exitosamente")
            return {"message": f"Optional method {selected_method} set for step {workflow_step}"}
        except Exception as e:
            logger.error(f"POST /stage2/set_optional_method - Error al establecer método {selected_method}: {str(e)}")
            abort(500, description=str(e))

@stage_2.route("/set_filter")
class SetFilterCollection(MethodView):
    @stage_2.arguments(WorkflowNameQuerySchema, location="query")
    @stage_2.arguments(WorkflowStepNameQuerySchema, location="query")
    @stage_2.arguments(WorkflowStepMethodNameQuerySchema, location="query")
    @stage_2.arguments(FilterRequestSchema, location="json")
    @stage_2.response(status_code=200, schema=FilterAppliedSchema)
    def post(self, workflow_args, step_args, method_args, json_data):
        """Aplica filtros a un método específico"""
        workflow_name = workflow_args["workflow_name"]
        workflow_step = step_args["workflow_step_name"]
        method_name = method_args["workflow_step_method_name"]
        filters = json_data["filters"]
        logger.info(f"POST /stage2/set_filter - Aplicando filtros al método {method_name} en step {workflow_step} workflow {workflow_name}")
        try:
            orchestrator.set_filter_to_method(filters, method_name, workflow_step, workflow_name)
            logger.info(f"POST /stage2/set_filter - Filtros aplicados exitosamente al método {method_name}")
            return {"message": f"Filter applied to method {method_name} in step {workflow_step}"}
        except Exception as e:
            logger.error(f"POST /stage2/set_filter - Error al aplicar filtros al método {method_name}: {str(e)}")
            abort(500, description=str(e))

@stage_2.route("/set_search_param")
class SetSearchParamCollection(MethodView):
    @stage_2.arguments(WorkflowNameQuerySchema, location="query")
    @stage_2.arguments(SearchParamRequestSchema, location="json")
    @stage_2.response(status_code=200, schema=SearchParamSetSchema)
    def post(self, workflow_args, json_data):
        """Establece el parámetro de búsqueda para un workflow"""
        workflow_name = workflow_args["workflow_name"]
        search_term = json_data["search_id"]
        logger.info(f"POST /stage2/set_search_param - Estableciendo parámetro de búsqueda '{search_term}' para workflow {workflow_name}")
        try:
            orchestrator.set_workflow_search_param(search_term, workflow_name)
            logger.info(f"POST /stage2/set_search_param - Parámetro de búsqueda establecido exitosamente para {workflow_name}")
            return {"message": f"Search parameter '{search_term}' set for workflow {workflow_name}"}
        except Exception as e:
            logger.error(f"POST /stage2/set_search_param - Error al establecer parámetro para {workflow_name}: {str(e)}")
            abort(500, description=str(e))

@stage_2.route("/set_stage_3")
class SetStage3Collection(MethodView):
    @stage_2.arguments(WorkflowNameQuerySchema, location="query")
    @stage_2.response(status_code=200, schema=SetStage3Schema)
    def post(self, workflow_args):
        """Cambia el workflow al stage 3"""
        workflow_name = workflow_args["workflow_name"]
        logger.info(f"POST /stage2/set_stage_3 - Cambiando workflow {workflow_name} a stage 3")
        try:
            orchestrator.set_stage_3(workflow_name)
            logger.info(f"POST /stage2/set_stage_3 - Workflow {workflow_name} cambiado exitosamente a stage 3")
            return {"message": f"Workflow {workflow_name} set to stage 3"}
        except Exception as e:
            logger.error(f"POST /stage2/set_stage_3 - Error al cambiar workflow {workflow_name} a stage 3: {str(e)}")
            abort(500, description=str(e))

# Stage 3 endpoints
@stage_3.route("/start_workflow")
class StartWorkflowCollection(MethodView):
    @stage_3.arguments(WorkflowNameQuerySchema, location="query")
    def post(self, workflow_args):
        """Inicia la ejecución del workflow y devuelve el resultado JSON sin schema predefinido CAMBIA A STAGE_1 AUTOMÁTICAMENTE"""
        workflow_name = workflow_args["workflow_name"]
        logger.info(f"POST /stage3/start_workflow - Iniciando ejecución del workflow {workflow_name}")
        try:
            results = orchestrator.start_workflow(workflow_name)
            logger.info(f"POST /stage3/start_workflow - Workflow {workflow_name} iniciado exitosamente")
            return {
                "workflow_name": workflow_name,
                "message": f"Workflow {workflow_name} started successfully",
                "status": "completed",
                "results": results,
            }, 200
        except Exception as e:
            logger.error(f"POST /stage3/start_workflow - Error al iniciar workflow {workflow_name}: {str(e)}")
            abort(500, description=str(e))

@stage_3.route("/set_stage_1")
class ResetToStage1Collection(MethodView):
    @stage_3.arguments(WorkflowNameQuerySchema, location="query")
    @stage_3.response(status_code=200, schema=SetStage1Schema)
    def post(self, workflow_args):
        """Resetea el workflow al stage 1"""
        workflow_name = workflow_args["workflow_name"]
        logger.info(f"POST /stage3/set_stage_1 - Reseteando workflow {workflow_name} a stage 1")
        try:
            orchestrator.set_stage_1(workflow_name)
            logger.info(f"POST /stage3/set_stage_1 - Workflow {workflow_name} reseteado exitosamente a stage 1")
            return {"message": f"Workflow {workflow_name} reset to stage 1"}
        except Exception as e:
            logger.error(f"POST /stage3/set_stage_1 - Error al resetear workflow {workflow_name}: {str(e)}")
            abort(500, description=str(e))

#Debajo del proyecto
api.register_blueprint(stage_1)
api.register_blueprint(stage_2)
api.register_blueprint(stage_3)

workflows = [Workflow()]
orchestrator = Orchestrator(workflows)
