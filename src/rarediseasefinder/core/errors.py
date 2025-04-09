class BaseError(Exception):
    """Excepción base para errores"""
    pass

class BaseHTTPError(BaseError):
    """Error de comunicación con la API"""
    pass

class BaseParsingError(BaseError):
    """Error al procesar datos"""
    pass