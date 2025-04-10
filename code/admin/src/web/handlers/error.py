from dataclasses import dataclass
from flask import render_template
from src.web.handlers import error

@dataclass
class Error:
    code: int
    message: str
    description: str

def register(app):
    """Registro de errores"""
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(500, error.internal_server_error)
    app.register_error_handler(400, error.bad_request_400)
    app.register_error_handler(401, error.unauthorized_401)
    app.register_error_handler(403, error.forbidden_403)

def not_found_error(e):
    error = Error(404,"Not Found","La URL solicitada no se encontró en el servidor.")
    return render_template("error.html", error=error), error.code

def internal_server_error(e):
    error = Error(500, "Internal Server Error", "Hubo un problema en el servidor.")
    return render_template("error.html", error=error), error.code

def bad_request_400(e):
    error = Error(400, "Bad Request", "La solicitud no se puede procesar debido a un error del cliente.")
    return render_template("error.html", error=error), error.code

def unauthorized_401(e):
    error = Error(401, "Unauthorized", "No tienes autorización para acceder a este recurso.")
    return render_template("error.html", error=error), error.code

def forbidden_403(e):
    error = Error(403, "Forbidden", "No tienes permiso para acceder a esta página.")
    return render_template("error.html", error=error), error.code
