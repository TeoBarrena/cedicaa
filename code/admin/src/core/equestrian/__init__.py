from flask import session
from src.core.database import db
from src.core.equestrian.horse import Horse
from src.core import employees
from datetime import datetime

def list_horses(page, per_page, name='', rider_type='', sort_by='nombre', order='asc'):
    """Retorna la lista de caballos paginando por página con filtros y ordenación."""
    
    # Construir la consulta base
    query = Horse.query

    # Aplicar filtro por estado activo
    query = query.filter(Horse.is_active == True)
    
    # Aplicar filtro por nombre
    if name:
        query = query.filter(Horse.name.ilike(f'%{name}%'))
    
    # Aplicar filtro por tipo de jinete
    if rider_type:
        query = query.filter(Horse.rider_type == rider_type)
    
    # Aplicar ordenación
    if sort_by == 'name':
        query = query.order_by(Horse.name.asc() if order == 'asc' else Horse.name.desc())
    elif sort_by == 'birthdate': 
        query = query.order_by(Horse.birthdate.asc() if order == 'asc' else Horse.birthdate.desc())
    elif sort_by == 'entry_date': 
        query = query.order_by(Horse.entry_date.asc() if order == 'asc' else Horse.entry_date.desc())

    # Retornar la paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def create(employee_ids, **kwargs):
    """Crea un nuevo caballo"""
    horse = Horse(**kwargs)
    if employee_ids is not None:
        horse.employees.extend(employees.get_multiple_employees_by_ids(employee_ids))
    db.session.add(horse)
    db.session.commit()
    return horse

def show(id_horse):
    """Retorna la información de un caballo"""
    return get_horse_by_id(id_horse)
    
def update(id_horse, employee_ids, **kwargs):
    """Actualiza la información de un caballo """
    horse = get_horse_by_id(id_horse)
    current_employees = get_associated_employees(id_horse)

    new_employee_ids = [emp for emp in employee_ids if emp not in current_employees]
    old_employee_ids = [emp for emp in current_employees if emp not in employee_ids]

    # Agregar nuevos empleados
    for emp_id in new_employee_ids:
        employee = employees.find_employee_by_id(emp_id) 
        horse.employees.append(employee)

    # Eliminar empleados que ya no están seleccionados
    for emp_id in old_employee_ids:
        employee = employees.find_employee_by_id(emp_id) 
        horse.employees.remove(employee)

    for key, value in kwargs.items():
        setattr(horse, key, value) 
    db.session.commit()
    return horse

def destroy(id_horse):
    """Eliminación lógica de un caballo"""
    horse = get_horse_by_id(id_horse)
    horse.is_active=False
    db.session.commit()

def get_horse_by_id(id_horse):
    """Retorna un caballo de la base de datos por su id"""
    return Horse.query.get(id_horse)

def is_deleted(id_horse):
    """Verifica si un caballo ha sido eliminado"""
    return Horse.query.get(id_horse).is_active == False

def get_employees(id_horse):
    """Retorna la lista de empleados asociados a un caballo"""
    return Horse.query.get(id_horse).employees

def get_associated_employees(id_horse):
    """Retorna la lista de los ids de los empleados asociados a un caballo"""
    employees = get_employees(id_horse)
    return [employee.id for employee in employees] 

def is_different(horse_data, id_horse, updated_trainer_ids):
    """Verifica si los datos de un caballo han cambiado"""
    horse = get_horse_by_id(id_horse)
    return (horse.name != horse_data['name'] or 
            horse.birthdate != datetime.strptime(horse_data['birthdate'], '%Y-%m-%d')  or
            horse.gender != horse_data['gender'] or
            horse.breed != horse_data['breed'] or
            horse.fur != horse_data['fur'] or
            horse.acquisition != horse_data['acquisition'] or
            horse.entry_date != datetime.strptime(horse_data['entry_date'], '%Y-%m-%d')  or
            horse.assigned_headquarters != horse_data['assigned_headquarters'] or
            horse.rider_type != horse_data['rider_type'] or
            set(get_associated_employees(id_horse)) != set(updated_trainer_ids)
            )

def update_files(id_horse, **kwargs):
    """Actualiza los archivos de un caballo"""
    horse = get_horse_by_id(id_horse)
    for key, value in kwargs.items():
        setattr(horse, key, value)
    db.session.commit()

def get_file_path(fieldname, horse_id):
    """Retorna la ruta de un archivo de un caballo"""
    horse = get_horse_by_id(horse_id)
    if horse is None:
        return None
    return getattr(horse, fieldname)
