from src.core.database import db

class Horse (db.Model):
    __tablename__ = "horse"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    breed = db.Column(db.String(30), nullable=False)
    fur = db.Column(db.String(30), nullable=False)
    acquisition = db.Column(db.String(30), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)
    assigned_headquarters = db.Column(db.String(30), nullable=False)
    rider_type = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Define la relación con la tabla de empleados
    employees = db.relationship('Employee', secondary='horse_employee', backref=db.backref('horses', lazy='dynamic'))
    
    # Tabla de asociación
    horse_employee = db.Table('horse_employee',
        db.Column('horse_id', db.Integer, db.ForeignKey('horse.id'), primary_key=True),
        db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    )

    #Archivos con información complementaria
    general_information = db.Column(db.String(255), default = None, nullable=True)
    training_schedule = db.Column(db.String(255), default = None, nullable=True)
    progress_report = db.Column(db.String(255), default = None, nullable=True)
    vet_records = db.Column(db.String(255), default = None, nullable=True)
    image_1 = db.Column(db.String(255), default = None, nullable=True)
    image_2 = db.Column(db.String(255), default = None, nullable=True)
    image_3 = db.Column(db.String(255), default = None, nullable=True)
    image_4 = db.Column(db.String(255), default = None, nullable=True)
    image_5 = db.Column(db.String(255), default = None, nullable=True)
