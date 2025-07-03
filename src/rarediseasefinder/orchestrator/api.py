from flask import Flask
from flask_smorest import Api, Blueprint

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

todo = Blueprint("workflows", "workflows", url_prefix="/workflows",description="workflows API")


workflows = [
    {
        "workflow_name": "Pharos",
        "workflow_description": "Fetches x data from Pharos API x data from selleckchem",
        "status": True,

    }
]

workflow_step = [
    {
        "workflow_step_name":"",
        "workflow_step_description":"",

    }
]