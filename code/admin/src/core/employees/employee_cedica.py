from datetime import datetime
from sqlalchemy import Date
from src.core.database import db
from src.core.auth import User
from src.core.jinete_amazonas.jinete_amazonas import Province, Town 

class Employee(db.Model):
    __tablename__ = "employees"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    dni = db.Column(db.String(15),nullable=False)
    email = db.Column(db.String(50), nullable=False)

    address = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable = False)
    departament = db.Column(db.String(20), nullable = True)

    town_id = db.Column(db.Integer, db.ForeignKey('town.id'), nullable=False)
    town = db.relationship('Town')

    phone = db.Column(db.String(20),nullable=False)

    profession = db.Column(db.String(40), nullable=False)
    job_position = db.Column(db.String(40), nullable=False)
    
    start_date = db.Column(db.Date, default=datetime.now().date)
    termination_date = db.Column(db.Date, nullable=True)
    
    inserted_at = db.Column(db.Date, default=datetime.now().date)

    emergency_contact_name = db.Column(db.String(20), nullable =False)
    emergency_contact_phone = db.Column(db.String(20), nullable =False)

    social_work = db.Column(db.String(40), nullable=False) #este atributo es obra social
    afilliate_number = db.Column(db.Integer, nullable=False)

    condition = db.Column(db.Enum('Voluntario', 'Personal Rentado', name="employee_condition"), nullable=False)

    active = db.Column(db.Boolean, default= True, nullable=False)

    #la relación con un usuario es opcional
    user = db.relationship('User', back_populates='employee', uselist=False)

    # Relación inversa con PaymentRecord, no aparece en la bd esto como un atributo, tmpcp el de user
    payment_records = db.relationship('PaymentRecord', back_populates='employee', lazy='dynamic')

    #archivos con documentación complementaria
    title = db.Column(db.String(255), default = None, nullable=True)
    dni_copy = db.Column(db.String(255), default = None, nullable=True)
    updated_cv = db.Column(db.String(255), default = None, nullable=True)

    is_deleted = db.Column(db.Boolean, default=False)
    

    def __repr__(self):
        return f'<Employee {self.name} {self.lastname}, {self.profession}>'
