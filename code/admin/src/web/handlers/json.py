from functools import wraps
from werkzeug.exceptions import BadRequest
from flask import request, jsonify
import json

def handle_bad_json(func):
    """
    Manejador para JSON mal formado. La función decorada debe recibir un diccionario (json) 
    como primer argumento.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            json_data = request.get_json()
        except (json.JSONDecodeError, TypeError) as e:
            return jsonify({"error": "JSON mal formado."}), 400
        except (BadRequest):
            return jsonify({"error": "JSON mal formado."}), 400
        return func(json_data, *args, **kwargs)
    return wrapper