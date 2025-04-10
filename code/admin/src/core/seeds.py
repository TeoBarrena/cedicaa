from src.core.auth import User
from datetime import datetime, timedelta
from src.core.jinete_amazonas import create_new_rider, create_new_school, create_new_relative, create_new_document
from src.core import auth, employees, equestrian, messages
from src.core.database import db
from src.core.jinete_amazonas.utils import PROVINCE_TOWNS
from src.core.jinete_amazonas.jinete_amazonas import Province, Town
from datetime import datetime
from src.core.payment_record.payment_record import PaymentRecord
from src.core.collection_record import create_new_collection
from src.core.publications import create_publication
import random

def generate_random_date(start_date, end_date):
    """Genera una fecha aleatoria entre dos fechas dadas."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def load_sample_collections():
    """Carga entre 20 y 30 cobros en la base de datos, con fechas distribuidas entre febrero de 2023 y octubre de 2024."""
    start_date = datetime(2023, 2, 1)
    end_date = datetime(2024, 10, 31)
    payment_methods = ['Credit Card', 'Cash', 'Bank Transfer']
    employee_ids = [1, 2, 3]  # Ajusta esto según los IDs de empleados disponibles

    for _ in range(random.randint(20, 30)):
        collection_data = {
            'rider_id': random.choice([1, 2, 3]),
            'payment_date': generate_random_date(start_date, end_date),
            'payment_method': random.choice(payment_methods),
            'amount': round(random.uniform(2000, 5000), 2),
            'received_by_id': random.choice(employee_ids),
            'notes': 'Cobro generado automáticamente',
            'is_pay': True,
            'is_deleted': False
        }
        create_new_collection(**collection_data)

    print("Carga de cobros completada.")

def seed_publications():
    statuses = ["Publicado", "Archivado", "Borrador"]
    authors = User.query.all()

    publications = [
        {
            "title": "La importancia de la salud mental en el trabajo",
            "summary": "Un enfoque en cómo mejorar el bienestar emocional en entornos laborales.",
            "content": "Hoy en día, la salud mental es un pilar fundamental para el éxito y la productividad. Este artículo explora estrategias prácticas para fomentar el equilibrio emocional en el trabajo.",
            "author": random.choice(authors),
            "creation_date": datetime(2023, 1, 10),
            "update_date": datetime(2023, 1, 15),
            "status": "Borrador",
        },
        {
            "title": "Tendencias tecnológicas para 2024",
            "summary": "Conoce las tecnologías que están marcando el rumbo este año.",
            "content": "Este año viene cargado de avances, desde la inteligencia artificial hasta el 5G. Descubre qué esperar en los próximos meses.",
            "author": random.choice(authors),
            "publication_date": datetime(2023, 10, 5, 12, 0),
            "creation_date": datetime(2023, 7, 1),
            "update_date": datetime(2023, 9, 30),
            "status": "Publicado",
        },
        {
            "title": "Historia de la inteligencia artificial",
            "summary": "Un repaso a los hitos más importantes de la IA.",
            "content": "Desde Alan Turing hasta los algoritmos modernos de aprendizaje profundo, este artículo detalla los eventos clave en el desarrollo de la inteligencia artificial.",
            "author": random.choice(authors),
            "publication_date": datetime(2023, 5, 10, 10, 0),
            "creation_date": datetime(2023, 4, 20),
            "update_date": datetime(2023, 5, 1),
            "status": "Archivado",
        },
    ]

    for i in range(12):
        status = "Publicado" if i < 9 else random.choice(statuses[1:])  
        title = f"Publicación {i + 4}: Tema interesante {random.randint(1, 100)}"
        summary = f"Resumen de un tema intrigante relacionado con el artículo número {i + 4}."
        content = f"Este artículo aborda aspectos fascinantes sobre {title.lower()}."
        author = random.choice(authors)
        creation_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 200))
        update_date = creation_date + timedelta(days=random.randint(0, 30))
        publication_date = (
            creation_date + timedelta(days=random.randint(5, 60))
            if status == "Publicado"
            else None
        )

        publications.append({
            "title": title,
            "summary": summary,
            "content": content,
            "author": author,
            "creation_date": creation_date,
            "update_date": update_date,
            "publication_date": publication_date,
            "status": status,
        })

    for publication in publications:
        create_publication(
            title=publication["title"],
            summary=publication["summary"],
            content=publication["content"],
            author=publication["author"],
            creation_date=publication["creation_date"],
            update_date=publication["update_date"],
            publication_date=publication.get("publication_date"),
            status=publication["status"],
        )

def seed_payment_records():
    # Crea un registro de pago sin empleado asociado
    payment_record1 = PaymentRecord(
        amount=150.00,
        payment_type='Gastos varios',
        description='Pago de electricidad'
    )
    db.session.add(payment_record1)

    # Crea un registro de pago con empleado asociado
    payment_record2 = PaymentRecord(
        amount=500.00,
        payment_date = "2022-02-22",
        payment_type='Honorarios',
        description='Pago a empleado',
        employee_id=1  # Asegúrate de que este ID existe
    )
    db.session.add(payment_record2)

    payment_record3 = PaymentRecord(
        amount=100.00,
        payment_date = "2010-02-22",
        payment_type='Honorarios',
        description='Pago a empleado',
        employee_id=1  
    )
    db.session.add(payment_record3)

    payment_record4 = PaymentRecord(
        amount=500.00,
        payment_date = "2010-05-22",
        payment_type='Honorarios',
        description='Pago a empleado',
        employee_id=1  
    )
    db.session.add(payment_record4)
    db.session.commit()

def load_horses():
    # Crear caballos
    horse1 = equestrian.create(
        name="Trueno", birthdate=datetime(2018, 5, 12), gender="Macho", 
        breed="Árabe", fur="Bayo", acquisition="Compra", 
        entry_date=datetime(2020, 7, 15), assigned_headquarters="Establo A", 
        rider_type="Equitación", employee_ids=[]
    )

    horse2 = equestrian.create(
        name="Sombra", birthdate=datetime(2016, 4, 22), gender="Macho", 
        breed="Pura Sangre", fur="Negro", acquisition="Donación", 
        entry_date=datetime(2019, 8, 3), assigned_headquarters="Establo B", 
        rider_type="Hipoterapia", employee_ids=[12]
    )

    horse3 = equestrian.create(
        name="Espíritu", birthdate=datetime(2017, 3, 10), gender="Hembra", 
        breed="Cuarto de Milla", fur="Alazán", acquisition="Donación", 
        entry_date=datetime(2021, 9, 18), assigned_headquarters="Establo C", 
        rider_type="Monta Terapéutica", employee_ids=[11]
    )

    horse4 = equestrian.create(
        name="Llama", birthdate=datetime(2015, 2, 27), gender="Macho", 
        breed="Mustang", fur="Palomino", acquisition="Compra", 
        entry_date=datetime(2022, 10, 1), assigned_headquarters="Establo A", 
        rider_type="Deporte Ecuestre Adaptado", employee_ids=[]
    )

    horse5 = equestrian.create(
        name="Margarita", birthdate=datetime(2019, 7, 19), gender="Hembra", 
        breed="Appaloosa", fur="Manchado", acquisition="Donación", 
        entry_date=datetime(2023, 1, 14), assigned_headquarters="Establo B", 
        rider_type="Actividades Recreativas", employee_ids= [11, 12]
    )

def seeds_jinete_amazona():
    # Crear instituciones escolares (schools)
    school1 = create_new_school(name='Escuela Primaria N° 1', address='Calle 1', phone='123456789', current_grade=1)
    school2 = create_new_school(name='Escuela Secundaria N° 2', address='Calle 2', phone='987654321', current_grade=4)

    # Crear familiares (relatives)
    relative1 = create_new_relative(first_name='María', last_name='Pérez', dni='12345678', relationship='Madre', address='Calle 123', mobile='111222333', email='maria.perez@example.com', education='Universitario', occupation='Profesora')
    relative2 = create_new_relative(first_name='Juan', last_name='García', dni='87654321', relationship='Padre', address='Calle 456', mobile='999888777', email='juan.garcia@example.com', education='Secundario', occupation='Contador')

    # Crear jinetes o amazonas (riders)
    rider1 = create_new_rider(
        first_name='Ana',
        last_name='Gómez',
        dni='123456789',
        birth_date=datetime(2005, 5, 20),
        age=18,
        town_id=3,
        town_id_of_birth = 2,
        address="Calle Imaginaria X",
        number = "7777",
        apartment = "Depto Imag A",
        phone='123456789',
        emergency_contact='Laura Gómez',
        emergency_phone='1122334455',
        scholarship=True,
        scholarship_notes='Beca completa por buen rendimiento',
        has_disability_certificate=True,
        diagnosis='ECNE',
        other_diagnosis=None,
        disability_type='Motora',
        family_allowance=True,
        allowance_type='Asignación Universal por hijo',
        pension=False,
        pension_type=None,
        social_security='Obra Social N° 1',
        member_number='12345',
        cure=False,
        social_security_notes=None,
        school_id=school1.id,
        professionals='Dr. Rodríguez',
        relative_id1=relative1.id,
        relative_id2=None,
        proposal_type='Equitación',
        condition='DE BAJA',
        location='HLP',
        days='Lunes, Miércoles, Viernes',
        therapist_id=2,
        driver_id=3,
        horse_id=1,
        assistant_id=2,
    )

    rider2 = create_new_rider(
        first_name='Carlos',
        last_name='López',
        dni='987654321',
        birth_date=datetime(2010, 7, 15),
        age=14,
        town_id=4,
        town_id_of_birth = 10,
        address="Calle Imaginaria Y",
        number = "222",
        apartment = "Depto Imag B",
        phone='987654321',
        emergency_contact='Claudia López',
        emergency_phone='9988776655',
        scholarship=False,
        scholarship_notes=None,
        has_disability_certificate=True,
        diagnosis='Trastorno de la Comunicación',
        other_diagnosis=None,
        disability_type='Viscera, Sensorial',
        family_allowance=False,
        allowance_type=None,
        pension=True,
        pension_type='Provincial',
        social_security='Obra Social N° 2',
        member_number='67890',
        cure=True,
        social_security_notes='Asiste a terapia semanal',
        school_id=school2.id,
        professionals='Dr. Martínez',
        relative_id1=relative2.id,
        relative_id2=None,
        proposal_type='Actividades Recreativas',
        condition='REGULAR',
        location='OTRO',
        days='Martes, Jueves',
        therapist_id=1,
        driver_id=2,
        horse_id=3,
        assistant_id=1,
    )

    rider3 = create_new_rider(
        first_name='Juan',
        last_name='García',
        dni='31221214',
        birth_date=datetime(2000, 9, 12),
        age=24,
        town_id=123,
        town_id_of_birth = 125,
        address="Calle Imaginaria Z",
        number = "10",
        phone='221 9821341',
        emergency_contact='Pedro Lugonez',
        emergency_phone='221 2134432',
        scholarship=False,
        scholarship_notes=None,
        has_disability_certificate=True,
        diagnosis='Trastorno de la Comunicación',
        other_diagnosis=None,
        disability_type='Mental',
        family_allowance=False,
        allowance_type=None,
        pension=True,
        pension_type='Nacional',
        social_security='IOMA',
        member_number='9876875',
        cure=True,
        social_security_notes='Asiste a terapia semanal',
        school_id=school2.id,
        professionals='Dr. Perez disabal',
        relative_id1=relative2.id,
        relative_id2=None,
        proposal_type='Actividades Recreativas',
        condition='REGULAR',
        location='OTRO',
        days='Martes, Jueves, Domingo',
        therapist_id=1,
        driver_id=2,
        horse_id=3,
        assistant_id=1,
    )

    collection1 = create_new_collection(
        rider_id=1,
        amount=1500.00,
        notes='Paga en la semana.',
        is_pay=False,
        is_deleted=False
    )

    collection2 = create_new_collection(
        rider_id=2,
        payment_method='Transferencia',
        amount=3500.00,
        notes='Pago completo por Mercado Pago.',
        payment_date=datetime(2023, 11, 4),
        received_by_id=11,
        is_pay=True,
        is_deleted=False
    )

    collection4 = create_new_collection(
        rider_id=3,
        amount=1500.00,
        notes='Debe 2 meses',
        is_pay=False,
        is_deleted=False
    )

    document1 = create_new_document(
                rider_id=1,
                title="GitLab",
                document_type="entrevista",
                file_path="https://gitlab.catedras.linti.unlp.edu.ar/",
                is_external=True
            )
    
    document2 = create_new_document(
                rider_id=2,
                title="Chatgpt",
                document_type="evolución",
                file_path="https://chatgpt.com/",
                is_external=True
            )
    
    document3 = create_new_document(
                rider_id=3,
                title="GitHub",
                document_type="planificaciones",
                file_path="https://github.com//",
                is_external=True
            )


def run():
    # Inicializar roles y permisos
    auth.initialize_roles_and_permissions()
    messages.seed_messages()
    load_horses()


    for province_name, towns in PROVINCE_TOWNS.items():
        # Crear una nueva provincia
        province = Province(name=province_name)
        db.session.add(province)
        db.session.flush()  # Obtener el ID de la provincia

        # Crear ciudades relacionadas a la provincia
        for town in towns:
            town_entry = Town(name=town['name'], province_id=province.id)
            db.session.add(town_entry)
    
    # Confirmar los cambios
    db.session.commit()
    print("Provincias y localidades cargadas exitosamente.")
    
    new_data_1 = {"name": "Juan", "lastname": "Pérez", "dni": 12345678, 
    "email": "juan.perez@mail.com", "town_id": "1", "phone": "111111111", 
    "profession": "Psicólogo/a", "job_position": "Administrativo/a", 
    "emergency_contact_name": "María Pérez", "emergency_contact_phone": "12345678", 
    "social_work": "Obra Social X", "afilliate_number": 11111, "condition": "Personal Rentado", 
    "address": "Calle Falsa", "number": 123, "inserted_at": "2023-10-12"}

    new_data_2 = {"name": "Ana", "lastname": "García", "dni": 87654321, 
        "email": "ana.garcia@mail.com", "town_id": "1", "phone": "222222222", 
        "profession": "Psicólogo/a", "job_position": "Administrativo/a", 
        "emergency_contact_name": "Carlos García", "emergency_contact_phone": "23456789", 
        "social_work": "Obra Social Y", "afilliate_number": 22222, "condition": "Personal Rentado", 
        "address": "Avenida Siempre Viva", "number": 456, "inserted_at": "2023-09-24"}

    new_data_3 = {"name": "Lucía", "lastname": "Fernández", "dni": 34567890, 
        "email": "lucia.fernandez@mail.com", "town_id": "1", "phone": "333333333", 
        "profession": "Psicólogo/a", "job_position": "Administrativo/a", 
        "emergency_contact_name": "José Fernández", "emergency_contact_phone": "34567890", 
        "social_work": "Obra Social Z", "afilliate_number": 33333, "condition": "Personal Rentado", 
        "address": "Calle 79", "number": 789, "inserted_at": "2022-12-17"}

    new_data_4 = {"name": "Roberto", "lastname": "Martínez", "dni": 56789012, 
        "email": "roberto.martinez@mail.com", "town_id": "1", "phone": "444444444", 
        "profession": "Psicólogo/a", "job_position": "Administrativo/a", 
        "emergency_contact_name": "Julia Martínez", "emergency_contact_phone": "45678901", 
        "social_work": "Obra Social X", "afilliate_number": 44444, "condition": "Personal Rentado", 
        "address": "Calle Las Flores", "number": 555, "inserted_at": "2023-05-01"}

    new_data_5 = {"name": "Mariana", "lastname": "Gómez", "dni": 65432109, 
    "email": "mariana.gomez@mail.com", "town_id": "1", "phone": "555555555", 
    "profession": "Trabajadora Social", "job_position": "Coordinadora", 
    "emergency_contact_name": "Laura Gómez", "emergency_contact_phone": "56789012", 
    "social_work": "Obra Social A", "afilliate_number": 55555, "condition": "Personal Rentado", 
    "address": "Calle Los Pinos", "number": 102, "inserted_at": "2023-07-15"}

    new_data_6 = {"name": "Pedro", "lastname": "Ramírez", "dni": 32165498, 
        "email": "pedro.ramirez@mail.com", "town_id": "1", "phone": "666666666", 
        "profession": "Fonoaudiólogo/a", "job_position": "Entrenador de Caballos", 
        "emergency_contact_name": "Andrea Ramírez", "emergency_contact_phone": "67890123", 
        "social_work": "Obra Social B", "afilliate_number": 66666, "condition": "Personal Rentado", 
        "address": "Calle San Martín", "number": 304}

    new_data_7 = {"name": "Sofía", "lastname": "López", "dni": 78901234, 
        "email": "sofia.lopez@mail.com", "town_id": "1", "phone": "777777777", 
        "profession": "Psicopedagogo/a", "job_position": "Asistente", 
        "emergency_contact_name": "Diego López", "emergency_contact_phone": "78901234", 
        "social_work": "Obra Social C", "afilliate_number": 77777, "condition": "Personal Rentado", 
        "address": "Avenida Los Olivos", "number": 678, "inserted_at": "2023-11-08"}

    new_data_8 = {"name": "Lucas", "lastname": "Méndez", "dni": 12309876, 
        "email": "lucas.mendez@mail.com", "town_id": "1", "phone": "888888888", 
        "profession": "Fonoaudiólogo/a", "job_position": "Terapeuta", 
        "emergency_contact_name": "Carla Méndez", "emergency_contact_phone": "89012345", 
        "social_work": "Obra Social D", "afilliate_number": 88888, "condition": "Personal Rentado", 
        "address": "Calle Las Acacias", "number": 999, "inserted_at": "2023-06-30"}

    new_data_9 = {"name": "Julia", "lastname": "Cruz", "dni": 90876543, 
        "email": "julia.cruz@mail.com", "town_id": "1", "phone": "999999999", 
        "profession": "Docente", "job_position": "Asistente", 
        "emergency_contact_name": "Luis Cruz", "emergency_contact_phone": "90123456", 
        "social_work": "Obra Social E", "afilliate_number": 99999, "condition": "Personal Rentado", 
        "address": "Calle Los Álamos", "number": 203, "inserted_at": "2022-03-10"}

    new_data_10 = {"name": "Esteban", "lastname": "Paredes", "dni": 34567891, 
        "email": "esteban.paredes@mail.com", "town_id": "1", "phone": "101010101", 
        "profession": "Veterinario/a", "job_position": "Veterinario", 
        "emergency_contact_name": "Santiago Paredes", "emergency_contact_phone": "12345679", 
        "social_work": "Obra Social F", "afilliate_number": 101010, "condition": "Personal Rentado", 
        "address": "Calle Del Bosque", "number": 501, "inserted_at": "2023-09-01"}

    new_data_11 = {"name": "Martín", "lastname": "Ruiz", "dni": 45678912, 
        "email": "martin.ruiz@mail.com", "town_id": "1", "phone": "111111112", 
        "profession": "Profesor", "job_position": "Profesor de Equitación", 
        "emergency_contact_name": "Ana Ruiz", "emergency_contact_phone": "23456780", 
        "social_work": "Obra Social G", "afilliate_number": 111111, "condition": "Personal Rentado", 
        "address": "Calle La Pradera", "number": 404, "inserted_at": "2023-05-23"}    
    
    new_data_12= {"name":"Juana", "lastname":"Perez", "dni":777777, 
        "email":"empleadoprueba120@mail.com", "town_id":"1", "phone":"111111111", 
        "profession":"Psicólogo/a", "job_position":"Administrativo/a", 
        "emergency_contact_name":"AA", "emergency_contact_phone":"12345678", 
        "social_work":"Obra Social X", "afilliate_number":11111, "condition":"Personal Rentado", 
        "address":"Calle 79", "number":66}    
    
    #agrego 3 para que se vea que los formularios de jya funcionan 
    new_data_13 = {"name": "Carolina", "lastname": "Gómez", "dni": 35897465,
        "email": "carolina.gomez@mail.com", "town_id": "1", "phone": "222333444", 
        "profession": "Psicólogo/a", "job_position": "Terapeuta", 
        "emergency_contact_name": "Miguel Gómez","emergency_contact_phone": "44556677", 
        "social_work": "Obra Social A", "afilliate_number": 98765, "condition": "Personal Rentado",
        "address": "Calle Arboleda", "number": 102}

    new_data_14 = {"name": "Felipe", "lastname": "Lopez", "dni": 45632187,
        "email": "felipe.lopez@mail.com", "town_id": "1", "phone": "333444555",
        "profession": "Terapista Ocupacional", "job_position": "Auxiliar de Pista",
        "emergency_contact_name": "Laura Lopez", "emergency_contact_phone": "77889900",
        "social_work": "Obra Social B", "afilliate_number": 54321,
        "condition": "Personal Rentado", "address": "Calle Las Flores",
        "number": 78}

    new_data_15 = {"name": "Juan", "lastname": "Gonzalez", "dni": 45632187,
        "email": "Juan.gonzalez@mail.com", "town_id": "1", "phone": "22145442",
        "profession": "Profesor", "job_position": "Conductor",
        "emergency_contact_name": "Laura Lopez", "emergency_contact_phone": "33456789",
        "social_work": "Obra Social C", "afilliate_number": 221455,
        "condition": "Personal Rentado", "address": "Calle alem",
        "number": 728}
    
    # Crear empleados con profesiones y posiciones laborales asignadas
    employee0 = employees.create_employee(new_data_1)

    employee1 = employees.create_employee(new_data_2)

    employee2 = employees.create_employee(new_data_3)

    employee3 = employees.create_employee(new_data_4)

    employee4 = employees.create_employee(new_data_5)

    employee5 = employees.create_employee(new_data_6)

    employee6 = employees.create_employee(new_data_7)

    employee7 = employees.create_employee(new_data_8)

    employee8 = employees.create_employee(new_data_9)

    employee9 = employees.create_employee(new_data_10)

    employee10 = employees.create_employee(new_data_11)

    employee11 = employees.create_employee(new_data_12)

    employee12 = employees.create_employee(new_data_13)

    employee13 = employees.create_employee(new_data_14)
    
    employee14 = employees.create_employee(new_data_15)

    # Crear usuarios relacionados con el empleado

    system_admin = auth.create_user(employee_id=employee1.id, email="systemadmin@mail.com", password="1234", alias="Juan Admin", role="System Admin", inserted_at=datetime(2024, 3, 5))
    system_admin2 = auth.create_user(employee_id=employee0.id, email="systemadmin2@mail.com", password="1234", alias="Administrador", role="System Admin", inserted_at=datetime(2023, 1, 2))
    
    admin1 = auth.create_user(employee_id=employee2.id, email="admin1@mail.com", password="1234", alias="a1", role="Administration", inserted_at=datetime(2024, 7, 3))
    admin2 = auth.create_user(employee_id=employee3.id, email="admin2@mail.com", password="1234", alias="a2", role="Administration")
    
    tech1 = auth.create_user(employee_id=employee4.id, email="tech1@mail.com", password="1234", alias="t1", role="Technical", active=False, inserted_at=datetime(2024, 1, 4))
    tech2 = auth.create_user(employee_id=employee5.id, email="tech2@mail.com", password="1234", alias="t2", role="Technical")
    
    equestrian1 = auth.create_user(employee_id=employee6.id, email="equestrian1@mail.com", alias="e", password="1234", role="Equestrian", inserted_at=datetime(2024, 1, 5))
    # equestrian2 = auth.create_user(employee_id=employee7.id, email="equestrian2@mail.com", alias="e", password="1234", role="Equestrian")
    
    volunteer1 = auth.create_user(employee_id=employee8.id, email="volunteer1@mail.com", alias="v1", password="1234", role="Volunteer", inserted_at=datetime(2024, 9, 6))
    # volunteer2 = auth.create_user(employee_id=employee9.id, email="volunteer2@mail.com", alias="v2", password="1234", role="Volunteer")
    
    training = auth.create_user(employee_id=employee10.id, email="training@mail.com", alias="tra1", password="1234", role="Training", inserted_at=datetime(2024, 1, 12))
    
    user = auth.create_user(employee_id=employee11.id, email="user@mail.com", alias="user", password="1234")

    editor = auth.create_user(employee_id=employee12.id, email="editor@mail.com", password="1234", alias="ed1", role="Editor", inserted_at=datetime(2024, 1, 4))
    
    
    seed_payment_records()

    seeds_jinete_amazona()

    seed_publications()

    load_sample_collections()

    print("Datos cargados exitosamente!")

if __name__ == "__main__":
    run()
