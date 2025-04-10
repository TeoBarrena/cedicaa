from sqlalchemy import or_
from src.core.database import db
from src.core.jinete_amazonas.jinete_amazonas import Rider, Town, Province, School, Relative, RiderDocument
from src.core.equestrian import Horse
from src.core.auth import User
from src.core.employees.employee_cedica import Employee

def get_document_by_id(document_id):
    """Retorna un documento basado en su id."""
    return RiderDocument.query.get(document_id)

def get_riders_not_deleteds():
    """Retorna todos los jinete o amazona basado en su dni."""
    return Rider.query.filter_by(is_deleted=False)

def get_rider_by_dni(dni):
    """Retorna un jinete o amazona basado en su dni."""
    return Rider.query.filter_by(dni=dni).first()

def get_rider_by_id(rider_id):
    """Retorna un jinete o amazona basado en su ID."""
    return Rider.query.get(rider_id)


def get_relative_by_id(relative_id):
    """Retorna una familiar basado en su id."""
    return Relative.query.get(relative_id)

def delete_relative(relative_id):
    """Eliminación lógica de un Familiar"""
    relative = get_relative_by_id(relative_id)

    if not relative:
        raise ValueError("Familiar no encontrado")
    
    if relative.is_deleted:
        raise ValueError("El familiar ya estaba eliminado")
    
    relative.is_deleted = True

def get_school_by_id(school_id):
    """Retorna una Escuela basado en su id."""
    return School.query.get(school_id)

def delete_school(school_id):
    """Eliminación lógica de una Escuela"""
    school = get_school_by_id(school_id)

    if not school:
        raise ValueError("Escuela no encontrada")
    
    if school.is_deleted:
        raise ValueError("La Escuela ya estaba eliminada")
    
    school.is_deleted = True

def delete_rider(rider_id):
    """Eliminación lógica de un rider"""
    rider = get_rider_by_id(rider_id)

    if not rider:
        raise ValueError("Empleado no encontrado")
    
    if rider.is_deleted:
        raise ValueError("El empleado ya estaba eliminado")
    
    rider.is_deleted = True

    if rider.relative_id1: #en caso de q tenga un familiar asociado ejecuto el delete_relative
        delete_relative(rider.relative_id1)

    if rider.relative_id2: #en caso de q tenga un familiar asociado ejecuto el delete_relative
        delete_relative(rider.relative_id2)

    if rider.school_id: #en caso de q tenga una escuela asociada ejecuto el delete_school
        delete_school(rider.school_id)

    db.session.commit()
    return rider


def create_new_relative(**kwargs):
    """Crea un nuevo familiar de un Jinete o Amazonas en la base de datos"""
    
    relative = Relative(**kwargs)
    db.session.add(relative)
    db.session.commit()
    
    return relative

def create_new_school(**kwargs):
    """Crea una nueva escuela de un Jinete o Amazonas en la base de datos """
    
    school = School(**kwargs)
    db.session.add(school)
    db.session.commit()
    
    return school

def create_new_rider(**kwargs):
    """Crea un nuevo Jinete o Amazonas en la base de datos"""
    
    rider = Rider(**kwargs)
    db.session.add(rider)
    db.session.commit()
    
    return rider

def update_rider_bd():
    """Actualiza un Jinete o Amazonas en la base de datos"""
    db.session.commit()
    

def get_province_by_name(name):
    """Retorna un provincia basado en su nombre."""
    return Province.query.filter_by(name=name).first()

def get_towns_by_province(province_id):
    """Retorna las localidades basadas en su provincia."""
    return Town.query.filter_by(province_id=province_id).all()

def get_town_by_name(name, province):
    """Retorna una localidad basado en su nombre."""
    return Town.query.filter_by(name=name, province=province).first()



def show_list_riders(search_query, order_by,order_dir, page, per_page):
    """Muestra la lista de jinetes y amazonas permitiendo ordenarlos."""
    query = Rider.query.filter(Rider.is_deleted == False)

    # Agregar filtros de búsqueda
    if search_query:
        query = query.filter(
            or_(
                Rider.first_name.ilike(f"%{search_query}%"),
                Rider.last_name.ilike(f"%{search_query}%"),
                Rider.dni.ilike(f"%{search_query}%"),
                Rider.professionals.ilike(f"%{search_query}%")
            )
        )
    
    # Agregar ordenamiento
    if order_by == 'first_name':
        query = query.order_by(Rider.first_name.asc() if order_dir == 'asc' else Rider.first_name.desc())
    elif order_by == 'last_name':
        query = query.order_by(Rider.last_name.asc() if order_dir == 'asc' else Rider.last_name.desc())

    return query.paginate(page=page, per_page=per_page)



def get_institution_employees():
    """Retorna los empleados de la institucion segun su tipo."""
    employeers = Employee.query.filter(Employee.is_deleted == False)

    therapists = employeers.filter((Employee.job_position == 'Terapeuta') | (Employee.job_position == 'Profesor de equitación'))
    horses = Horse.query.filter(Horse.is_active == True).all()  # Filtrar también los caballos no eliminados
    drivers = employeers.filter(Employee.job_position == 'Conductor')
    assistants = employeers.filter(Employee.job_position == 'Auxiliar de Pista')

    return therapists, horses, drivers, assistants



def create_new_document(**kwargs):
    """Crea un nuevo Documento de un Jinete o Amazonas en la base de datos"""

    rider_document = RiderDocument(**kwargs)
    db.session.add(rider_document)
    db.session.commit()

def get_not_deleted_documents(rider_id, page, per_page, search_title='', document_type='', sort_by='uploaded_at', order='desc'):
    """Retorna los documentos de un rider segun su id."""
    query = RiderDocument.query.filter_by(rider_id=rider_id, is_deleted=False)
    
    if search_title:
        query = query.filter(RiderDocument.title.ilike(f'%{search_title}%'))
    
    if document_type:
        query = query.filter_by(document_type=document_type)
    
    if sort_by == 'title':
        query = query.order_by(RiderDocument.title.asc() if order == 'asc' else RiderDocument.title.desc())
    else:
        query = query.order_by(RiderDocument.uploaded_at.asc() if order == 'asc' else RiderDocument.uploaded_at.desc())
    
    return query.paginate(page=page, per_page=per_page, error_out=False)

def delete_document(document_id):
    """Elimina un documento de un Jinete o Amazona"""
    document = RiderDocument.query.get(document_id)
    document.is_deleted = True
    db.session.commit()
    return document

def get_riders_scholarship_data():
    """
    Consulta para contar la cantidad de becados y no becados
    """
    return db.session.query(
        Rider.scholarship,
        db.func.count()
    ).group_by(Rider.scholarship).filter(Rider.is_deleted == False).all()

def get_riders_dishability_type_data():
    """
    Consulta para contar la cantidad de J&A por tipo de discapacidad
    """
    return db.session.query(
        Rider.disability_type,
        db.func.count()
    ).group_by(Rider.disability_type).filter(Rider.is_deleted == False).all()

def get_riding_programs():
    """
    Retorna las propuestas de trabajo de los J&A ordenadas por cantidad de manera descendente
    """
    return db.session.query(
        Horse.rider_type,
        db.func.count(Horse.rider_type).label('count')
    ).join(
        Rider, Rider.horse_id == Horse.id
    ).filter(
        Rider.is_deleted == False
    ).group_by(
        Horse.rider_type
    ).order_by(
        db.func.count(Horse.rider_type).desc()
    ).all()