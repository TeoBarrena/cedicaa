from src.core.database import db
from sqlalchemy.sql import func
from src.core.auth.utils import ROLE_TRANSLATIONS

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  # Para la integridad referencial
    role = db.relationship("Role", back_populates="users")  # Para poder acceder al rol del usuario directamente
    
    inserted_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='user')

    
    def __repr__(self):
        return f'<User #{self.id} email="{self.email}" alias="{self.alias}" active="{self.active}">'

role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')),
    db.PrimaryKeyConstraint("role_id", "permission_id"),
)

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nombre del permiso, e.g., 'user_index'
    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')
    
    def __repr__(self):
        return f'<Permission #{self.id} name="{self.name}">'


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True) 
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary='role_permissions', back_populates='roles')
    
    def __repr__(self):
        return f'<Role #{self.id} name="{self.name}">'
    
    def get_translated_name(self):
        return ROLE_TRANSLATIONS.get(self.name, self.name)
