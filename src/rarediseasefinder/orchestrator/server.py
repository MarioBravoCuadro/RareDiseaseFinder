import enum
import uuid
from datetime import datetime, timezone

from flask import url_for, Flask, abort
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import fields, Schema

server = Flask(__name__)

class APIConfig:
    API_TITLE = "RareDiseaseFinder_API"
    API_VERSION = "V1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

server.config.from_object(APIConfig)

api = Api(server)

todo = Blueprint("todo", "todo", url_prefix="/todo",description="TODO API")

tasks = [
    {
        "id": uuid.UUID("92c97fbb-f467-4989-b146-99c152bd6bc5"),
        "created": datetime.now(timezone.utc),
        "completed": False,
        "task":"tarea 1",
    }
]

class CreateTask(Schema):
    task = fields.String()

class UpdateTask(CreateTask):
    completed = fields.Bool()

class Task(UpdateTask):
    id = fields.UUID()
    created = fields.DateTime()

class ListTasks(Schema):
    tasks = fields.List(fields.Nested(Task))

class SortByEnum(enum.Enum):
    task = "task"
    created = "created"

class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"

class ListTaskParameters(Schema):
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.created)
    order = fields.Enum(SortDirectionEnum,load_default=SortDirectionEnum.asc)

@todo.route("/tasks")
class TodoCollection(MethodView):
    @todo.arguments(ListTaskParameters, location = "query")
    @todo.response(status_code=200,schema=ListTasks)
    def get(self,parameters):
        return {
            "tasks" : sorted(
                tasks,
                key=lambda  task: task[parameters["order_by"].value],
                reverse=parameters["order"] == SortDirectionEnum.desc,
            )
        }

    @todo.response(status_code=201,schema=Task)
    def post(self,task):
        task["id"] = uuid.uuid4()
        task["created"] = datetime.now(timezone.utc)
        task["completed"] = False
        tasks.append(task)
        return task

@todo.route("/tasks/<uuid:task_id>")
class TodoItem(MethodView):

    @todo.response(status_code=200,schema=Task)
    def get(self,task_id):
        for task in tasks:
            if task["id"] == task_id:
                return task
        abort(404,f"Task with ID {task_id} not found.")

    @todo.arguments(UpdateTask)
    @todo.response(status_code=200,schema=Task)
    def put(self,task_id,payload):
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = payload["completed"]
                task["task"] = payload["task"]
                return task
        abort(404, f"Task with ID {task_id} not found.")

    @todo.response(status_code=204)
    def delete(self,task_id):
        for index, task in enumerate(tasks):
            tasks.pop(index)
            return
        abort(404, f"Task with ID {task_id} not found.")


#Debajo del proyecto
api.register_blueprint(todo)