from collections import OrderedDict
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from src.web.schemas.message import message_schema
from marshmallow import ValidationError
from src.core.messages.Message_model import Message
from src.core.database import db
from src.core.auth.captcha_config import verify_captcha
from src.web.handlers.json import handle_bad_json

bp = Blueprint("messages_api", __name__, url_prefix="/api/messages")

@bp.post("/")
@handle_bad_json
def create(json_data):
    
    try:
        new_message_json = {k: v for k, v in json_data.items() if k != "captcha"}
        new_message_data = message_schema.load(new_message_json)
    except ValidationError as err:
        return generate_response("Parámetros inválidos o faltantes en la solicitud.", 400, error=err.messages)

    captcha_response = json_data.get('captcha')  # Token de CAPTCHA enviado desde el frontend

    # Verificar CAPTCHA
    if not verify_captcha(captcha_response):
        return generate_response("Captcha inválido.", 400)

    new_message = Message(
        title=new_message_data['title'],
        email=new_message_data['email'],
        name=new_message_data['name'],
        body=new_message_data['body'],
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return generate_response("Consulta enviada exitosamente", 201, data=new_message)

def generate_response(message, status_code=200, data=None, error=None):
    response = OrderedDict()
    
    if error:
        response["error"] = message  
        response["details"] = error   
    else:
        response["message"] = message
        if data:
            response["data"] = {
                "title": data.title,  
                "email": data.email, 
                "body": data.body,  
            }
    
    return jsonify(response), status_code