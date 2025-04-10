from marshmallow import Schema, fields

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    email = fields.Str(required=True,
                    validate=lambda email: '@' in email,  
                    error_messages={"validator_failed": "El formato del correo es inválido."}) 
    name = fields.Str(required=True)
    body = fields.Str(required=True, validate=lambda body: len(body) >= 11, error_messages={"validator_failed": "El cuerpo del mensaje debe tener al menos 11 caracteres."})
    #captcha = fields.Str(required=True)
    inserted_at = fields.DateTime(dump_only=True)

message_schema = MessageSchema()
# para crear alguno personalizado:
# simple_message_schema = MessageSchema(only=("id", "email", "name", "body", "inserted_at"))