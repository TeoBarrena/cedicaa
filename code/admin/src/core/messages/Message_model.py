from src.core.database import db
from sqlalchemy.sql import func
from src.core.messages.utils import STATES_TRANSLATIONS

class Message(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(20), nullable=False, default="new")
    comment = db.Column(db.Text, nullable=True, default="")
    inserted_at = db.Column(db.DateTime, default=func.now())
    is_deleted = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        state = STATES_TRANSLATIONS.get(self.state, "Estado desconocido")
        return f'<Mensaje #{self.id}, titulo="{self.title}", email="{self.email}", estado="{state}">'