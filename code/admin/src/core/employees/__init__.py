from src.core.database import db
from src.core.jinete_amazonas.jinete_amazonas import Rider
from src.core.employees.employee_cedica import Employee
from sqlalchemy import or_, func, case, desc
from src.core.auth import delete_user

def list_employees(page, per_page, email='', name='', lastname='', dni='', active=None, sort_by='email', order='asc', job_position=''):
    """Retorna la lista de usuarios paginando por página con filtros y ordenación."""
    # Construir la consulta base
    query = Employee.query.filter_by(is_deleted=False)

    # Aplicar filtro por email
    if email:
        query = query.filter(Employee.email.ilike(f'%{email}%'))
    
    # Aplicar filtro por nombre
    if name:
        query = query.filter(Employee.name.ilike(f'%{name}%'))
    
    # Aplicar filtro por apellido
    if lastname:
        query = query.filter(Employee.lastname.ilike(f'%{lastname}%'))
    
    # Aplicar filtro por DNI
    if dni:
        query = query.filter(Employee.dni == dni)

    # Aplicar filtro por profesión
    if job_position:
        query = query.filter(Employee.job_position == job_position)

    # Aplicar filtro por estado activo
    if active is not None:
        query = query.filter(Employee.active == active)
    
    # Aplicar ordenación
    if sort_by == 'email':
        query = query.order_by(Employee.email.asc() if order == 'asc' else Employee.email.desc())
    elif sort_by == 'inserted_at': 
        query = query.order_by(Employee.inserted_at.asc() if order == 'asc' else Employee.inserted_at.desc())

    # Retornar la paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def list_employee_not_user():
    """Retorna lista de empleados que no tienen usuario asignado en el sistema"""
    return Employee.query.filter(Employee.user == None).all()

def find_employee_by_id(employee_id):
    """Busca un empleado por su ID"""
    return Employee.query.get(employee_id)

def find_employee_by_email(email):
    """Busca un empleado por su email"""
    return Employee.query.filter_by(email=email).first() #no se usa el metodo get, porque get busca por clave primarai

class EmailAlreadyExistsError(Exception):
    """Excepción para indicar que el email ya está registrado."""
    pass

def create_employee(new_data):
    """Crea un empleado y lo guarda en la base de datos."""
    new_email = new_data.get("email")
    existing_employee = find_employee_by_email(new_email)
    if existing_employee:
        raise ValueError("El email ya está registrado. Elija otro email.")
    
    # Actualizar los datos
    employee = Employee(**new_data)

    try:
        db.session.add(employee)
        db.session.commit()
        return employee
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error

def exists_employee_and_not_user(employee_id):
    """Verifica si existe un empleado y no tiene usuario asignado"""
    employee = find_employee_by_id(employee_id)
    if not employee:
        raise ValueError("Empleado no encontrado.")
    if employee.user:
        raise ValueError("El empleado ya tiene un usuario asignado.")
    return employee 

# show
def show(employee_id):
    """Retorna la información de un único empleado"""
    employee = Employee.query.get(employee_id)
    return employee

def has_not_changes(employee, updated_data):
    """Verifica si hay cambios en los datos del empleado."""
    
    updated_title = updated_data.get("title")
    updated_dni_copy = updated_data.get("dni_copy")
    updated_cv = updated_data.get("updated_cv")


    if updated_title is None:
        updated_title = 'No title'  # Maneja el caso donde no se envía un nuevo archivo

    if updated_dni_copy is None:
        updated_dni_copy = 'No updated_dni_copy'

    if updated_cv is None:
        updated_cv = 'No updated_cv'  # Maneja el caso donde no se envía un nuevo archivo

    # Ahora compara los atributos
    return (
        employee.name == updated_data.get("name") and
        employee.lastname == updated_data.get("lastname") and
        employee.dni == updated_data.get("dni") and
        employee.address == updated_data.get("address") and
        employee.number == int(updated_data.get("number")) and
        str(employee.departament) == updated_data.get("departament") and
        employee.town_id == int(updated_data.get("town_id")) and
        employee.email == updated_data.get("email") and
        employee.phone == updated_data.get("phone") and
        employee.emergency_contact_name == updated_data.get("emergency_contact_name") and
        employee.emergency_contact_phone == updated_data.get("emergency_contact_phone") and
        employee.social_work == updated_data.get("social_work") and
        employee.active == updated_data.get("active") and
        employee.condition == updated_data.get("condition") and
        employee.profession == updated_data.get("profession") and
        employee.job_position == updated_data.get("job_position") and
        employee.afilliate_number == int(updated_data.get("afilliate_number")) and
        str(employee.start_date) == updated_data.get("start_date") and  
        ((employee.termination_date is None and updated_data.get("termination_date") in [None, ""]) or (str(employee.termination_date) == updated_data.get("termination_date"))) and
        ((employee.title and updated_title == 'No title') or
        (employee.title == None and updated_title == 'No title')) and

        ((employee.dni_copy and updated_dni_copy == 'No updated_dni_copy') or
        (employee.dni_copy == None and updated_dni_copy == 'No updated_dni_copy')) and

        ((employee.updated_cv and updated_cv == 'No updated_cv') or
        (employee.updated_cv == None and updated_cv == 'No updated_cv'))

    )

def get_employees_not_deleteds():
    """Devuelve una lista de empleados que tienen el atributo 'is_deleted' en falso"""
    query = Employee.query.filter_by(is_deleted=False)
    return query


def save_files():
    """Guarda los datos en la BD"""
    db.session.commit()

def update_employee(employee, updated_data):
    """Actualiza la información de un empleado existente."""
    
    # Verificar si hay cambios
    if has_not_changes(employee, updated_data):
        raise ValueError("No se realizaron cambios en el perfil.")

    # Verificar el email único
    new_email = updated_data.get("email")
    if employee.email != new_email:
        existing_employee = find_employee_by_email(new_email)
        if existing_employee:
            raise ValueError("El email ya está registrado. Elija otro email.")
        
    # Actualizar los datos
    for key, value in updated_data.items():
        if key == "termination_date" and value == "":
            value = None
        setattr(employee, key, value)

    try:
        db.session.commit()
        return True, "Perfil actualizado correctamente"
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        return False, f"Error al actualizar el perfil: {str(e)}"


# destroy
def delete_employee(employee_id):
    """Elimina lógicamente a un empleado de la base de datos, en caso de tener asociado a un usuario, ejecuta el método delete_user del usuario correspondiente"""
    employee = find_employee_by_id(employee_id)

    if not employee:
        raise ValueError("Empleado no encontrado")
    
    if employee.is_deleted:
        raise ValueError("El empleado ya estaba eliminado")
    
    employee.is_deleted = True

    if employee.user: #en caso de q tenga un usuario asociado ejecuto el delete_user
        delete_user(employee.user.id)

    db.session.commit()
    return employee

def get_active_trainers():
    """Retorna la lista de empleados activos cuyo puesto laboral es 'Entrenador de Caballos' o 'Conductor'"""
    return Employee.query.filter_by(is_deleted = False).filter(
        or_(Employee.job_position == 'Entrenador de Caballos', Employee.job_position == 'Conductor')).all()

def get_multiple_employees_by_ids(employee_ids):
    """Retorna una lista de empleados por sus IDs"""
    return Employee.query.filter(Employee.id.in_(employee_ids)).all()


def asociate_user(employee,user):
    """Asocia un usuario a un empleado"""
    employee.user = user
    db.session.commit()
    return employee

def work_count(page, per_page):
    """
    Retorna la cantidad de casos en los que está trabajando cada profesional.
    Therapyst, Driver, Assistant
    """
    query = (
        db.session.query(
            Employee.dni.label("dni"),
            func.concat(Employee.name, " ", Employee.lastname).label("name_lastname"),
            func.count(case(
                (
                    (or_(
                        Rider.therapist_id == Employee.id,
                        Rider.driver_id == Employee.id,
                        Rider.assistant_id == Employee.id
                    ), 1)
                ),
                else_=None
            )).label("count"),
            Employee.profession.label("profession")
        )
        #Este es un left join que hace que se muestren todos los empleados, aunque no tengan casos asociados
        .outerjoin(Rider, or_(
            Rider.therapist_id == Employee.id,
            Rider.driver_id == Employee.id,
            Rider.assistant_id == Employee.id
        ))
        .group_by(Employee.id)
        .order_by(desc("count"))
    )

    return query.paginate(page=page, per_page=per_page, error_out=False)