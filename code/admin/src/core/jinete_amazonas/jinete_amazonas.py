from src.core.database import db
from datetime import datetime

class Province(db.Model):
    __tablename__ = 'province'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    towns = db.relationship('Town', back_populates='province')

    def __repr__(self):
        return f'<Province {self.name}>'

class Town(db.Model):
    __tablename__ = 'town'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    province_id = db.Column(db.Integer, db.ForeignKey('province.id'), nullable=False)
    province = db.relationship('Province', back_populates='towns', lazy=True)

    def __repr__(self):
        return f'<Town {self.name}, {self.province.name}>'
        
class Rider(db.Model):
    __tablename__ = 'rider'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)

    town_id = db.Column(db.Integer, db.ForeignKey('town.id'), nullable=False)
    town = db.relationship('Town', foreign_keys=[town_id])

    town_id_of_birth = db.Column(db.Integer, db.ForeignKey('town.id'), nullable=False)
    town_of_birth = db.relationship('Town', foreign_keys=[town_id_of_birth])

    address = db.Column(db.String(100), nullable=False) #address seria la calle, saque la tabla Address
    number = db.Column(db.Integer, nullable = False)
    apartment = db.Column(db.String(20), nullable = True)

    
    phone = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(100))   
    emergency_phone = db.Column(db.String(20))
    scholarship = db.Column(db.Boolean, default=False)
    scholarship_notes = db.Column(db.Text)
    has_disability_certificate = db.Column(db.Boolean, default=False)
    diagnosis = db.Column(db.String(255))
    other_diagnosis = db.Column(db.String(255))
    disability_type = db.Column(db.String(50))
    family_allowance = db.Column(db.Boolean, default=False)
    allowance_type = db.Column(db.String(100))
    pension = db.Column(db.Boolean, default=False)
    pension_type = db.Column(db.String(50))

    #SITUACIÓN PREVISIONAL
    social_security = db.Column(db.String(50))
    member_number = db.Column(db.String(50))
    cure = db.Column(db.Boolean, default=False)
    social_security_notes = db.Column(db.Text)

    #INSTITUCIÓN ESCOLAR a la que CONCURRE ACTUALMENTE:
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    school = db.relationship('School')

    #PROFESIONALES que lo ATIENDEN
    professionals = db.Column(db.Text, nullable=True)

    #DATOS PERSONALES De FAMILIAR/es O TUTOR/es RESPONSABLE/s:
    relative_id1 = db.Column(db.Integer, db.ForeignKey('relative.id'), nullable=False)
    relative_id2 = db.Column(db.Integer, db.ForeignKey('relative.id'))
    relative1 = db.relationship('Relative', foreign_keys=[relative_id1])
    relative2 = db.relationship('Relative', foreign_keys=[relative_id2])

    proposal_type = db.Column(db.String(100), nullable=False)  

    # Condición del jinete o amazona
    condition = db.Column(db.String(50), nullable=False)  

    # Sede de trabajo
    location = db.Column(db.String(50), nullable=False)  

    # Días seleccionados
    days = db.Column(db.String(100), nullable=True)  

    # Profesor o Terapeuta
    therapist_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)  
    therapist = db.relationship('Employee', foreign_keys=[therapist_id])

    # Conductor del Caballo
    driver_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)  
    driver = db.relationship('Employee', foreign_keys=[driver_id])

    # Caballo asignado
    horse_id = db.Column(db.Integer, db.ForeignKey('horse.id'), nullable=True)
    horse = db.relationship('Horse')

    # Auxiliar de Pista
    assistant_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    assistant = db.relationship('Employee', foreign_keys=[assistant_id])
    
    is_deleted = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Rider {self.first_name} {self.last_name}>'

class RiderDocument(db.Model):
    __tablename__ = 'rider_document'

    id = db.Column(db.Integer, primary_key=True)
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.id'), nullable=False)
    rider = db.relationship('Rider')

    title = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # entrevista, evaluación, etc.
    file_path = db.Column(db.String(255), nullable=True)  # Ruta del archivo subido
    uploaded_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    is_external = db.Column(db.Boolean, default=False)  # True si es un enlace externo
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<RiderDocument {self.title}>'
    
class School(db.Model):
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    address = db.Column(db.String(100), nullable=False)
    
    phone = db.Column(db.String(20))
    current_grade = db.Column(db.Integer)
    notes = db.Column(db.Text, nullable=True)

    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<School {self.name}, {self.phone}>'

class Relative(db.Model):
    __tablename__ = 'relative'

    id = db.Column(db.Integer, primary_key=True)
    relationship = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    education = db.Column(db.String(50))
    occupation = db.Column(db.String(100))

    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Relative {self.first_name} {self.last_name}>'