from flask import session
from sqlalchemy import asc, desc
from datetime import datetime
from src.core.database import db
from src.core.messages.Message_model import Message

def list_messages(page, per_page, email='', state=None, sort_by="inserted_at", order="desc"):
    """Consulta mensajes con filtros, orden y paginación."""
    query = Message.query.filter(Message.is_deleted == False)
    
    if email:
        query = query.filter(Message.email.ilike(f'%{email}%'))
        
    if state:
        query = query.filter(Message.state == state)

    if sort_by in ["inserted_at", "name", "email"]:
        order_function = asc if order == "asc" else desc
        query = query.order_by(order_function(getattr(Message, sort_by)))

    return query.paginate(page=page, per_page=per_page)

def find_message_by_id(message_id):
    """Busca un mensaje por su ID"""
    return Message.query.get(message_id)

def seed_messages():
    
    """Crea mensajes de prueba."""
    message1 = Message(
        title="Solicitud de información",
        email="usuario1@example.com",
        name="Juan Pérez",
        body="Hola, me gustaría recibir más información sobre los servicios que ofrecen. Gracias.",
        inserted_at=datetime(2024, 11, 17, 10, 30)
    )
    db.session.add(message1)
    
    message2 = Message(
        title="Consulta sobre productos",
        email="usuario2@example.com",
        name="Ana Gómez",
        body="Estoy interesada en comprar productos de su tienda. ¿Tienen algún descuento para compras al por mayor?",
        state="responded",
        comment="Mensaje respondido por el equipo de ventas.",
        inserted_at=datetime(2024, 11, 15, 14, 0)
    )
    db.session.add(message2)
    
    message3 = Message(
        title="Consulta rápida",
        email="usuario3@example.com",
        name="Carlos López",
        body="¿Puedo obtener más información?",
        inserted_at=datetime(2024, 11, 16, 9, 45) 
    )
    db.session.add(message3)

    message4 = Message(
        title="Queja sobre el servicio",
        email="usuario4@example.com",
        name="María Sánchez",
        body="El servicio estuvo muy por debajo de mis expectativas. Tuve que esperar más de una hora para ser atendida."
    )
    db.session.add(message4)
    
    message5 = Message(
        title="Sugerencia de mejora",
        email="usuario5@example.com",
        name="Pedro Ruiz",
        body="Sería útil tener un sistema para programar citas online. Me gustaría sugerirlo.",
        state="in_revision"
    )
    db.session.add(message5)
    
    db.session.commit()
    
    
def change_state(message, new_state):
    """
    Actualiza el estado del mensaje.
    """
    current_state = message.state
    if current_state == new_state:
        raise ValueError("El estado actual y el nuevo estado son iguales.")
    
    message.state = new_state
    db.session.commit()

def edit_comment(message, new_comment):
    """
    Edita el comentario del mensaje.
    """
    current_comment = message.comment
    if current_comment == new_comment:
        raise ValueError("El comentario actual y el nuevo comentario son iguales.")
    
    message.comment = new_comment
    
    if (message.state != "responded"):
        message.state = "responded"
    
    db.session.commit()

def destroy(message):
    """
    Eliminación lógica de una consulta/mensaje
    """
    message.is_deleted=True
    db.session.commit()