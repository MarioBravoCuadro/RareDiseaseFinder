from setuptools.errors import ExecError


class BaseError(Exception):
    """Excepción base para errores"""
    pass

class BaseHTTPError(BaseError):
    """Error de comunicación con la API"""
    pass

class BaseParsingError(BaseError):
    """Error al procesar datos"""
    pass

class IncorrectStageError(Exception):
    """Se ha ejecutado una llamada para una función que no coresponde con el stage disponible del workflow"""
    def __init__(self, current_stage: str, required_stage: str, operation: str = ""):
        self.current_stage = current_stage
        self.required_stage = required_stage
        self.operation = operation
        message = f"Operación '{operation}' no permitida. Workflow está en stage '{current_stage}' pero se requiere stage '{required_stage}'"
        super().__init__(message)
