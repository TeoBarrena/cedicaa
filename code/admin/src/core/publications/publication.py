from src.core.database import db
from datetime import datetime

class Publication(db.Model):
    __tablename__ = 'publications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    summary = db.Column(db.String(255), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User')

    publication_date = db.Column(db.DateTime) 
    creation_date = db.Column(db.DateTime, default=datetime.now()) 
    update_date = db.Column(db.DateTime, onupdate=datetime.now()) 
    
    is_deleted = db.Column(db.Boolean, default = False, nullable = False)

    status = db.Column(db.Enum('Borrador', 'Publicado', 'Archivado', name='publication_status'), default='Borrador')

    def __repr__(self):
        return f"<Publication {self.title}>"
