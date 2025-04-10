from flask import session
from src.core.database import db
from src.core.auth.user import User
from src.core.bcrypt import bcrypt
from src.core.auth.user import Role, Permission
from src.core.auth.utils import ROLE_PERMISSIONS, PERMISSIONS

def get_permissions(user): 
    """Retorna los permisos del rol que tiene asignado el usuario"""
    return ROLE_PERMISSIONS[user.role.name]

def is_system_admin(user):
    """Verifica si el usuario es un administrador del sistema"""
    return user.role.name == 'System Admin'

def list_users(page, per_page, email='', active=None, role='', sort_by='email', order='asc'):
    """Retorna la lista de usuarios paginando por página con filtros y ordenación."""
    
    # Construir la consulta base
    query = User.query.filter_by(is_deleted=False)
    
    # Aplicar filtro por email
    if email:
        query = query.filter(User.email.ilike(f'%{email}%'))
    
    # Aplicar filtro por estado activo
    if active is not None:
        query = query.filter(User.active == active)
    
    # Aplicar filtro por rol
    if role:
        query = query.join(User.role).filter(Role.name == role)
    
    # Aplicar ordenación
    if sort_by == 'email':
        query = query.order_by(User.email.asc() if order == 'asc' else User.email.desc())
    elif sort_by == 'inserted_at': 
        query = query.order_by(User.inserted_at.asc() if order == 'asc' else User.inserted_at.desc())

    # Retornar la paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_user(**kwargs):
    """Crea un nuevo usuario y guarda su contraseña encriptada en la base de datos"""
    email = kwargs.get('email')
    employee_id = kwargs.get('employee_id')
    
    from src.core import employees #lo movi para aca porque sino generaba import circular y eso daba error
    # Verificar si el empleado existe y no tiene un usuario asignado
    employees.exists_employee_and_not_user(employee_id)
    
    # Verificar si el usuario ya existe
    existing_user = find_user_by_email(email)
    if existing_user:
        raise ValueError("El email ya está registrado. Elija otro email.")
    
    #print(f"kwargs: {kwargs}")
    role_name = kwargs.pop('role', 'None')
    #print(f"role_name: {role_name}")
    role = get_role_by_name(role_name)
    #print(f"role: {role}")
    kwargs['role_id'] = role.id
    
    hash = bcrypt.generate_password_hash(kwargs['password'].encode('utf-8'))
    kwargs['password'] = hash.decode('utf-8')
    
    user = User(**kwargs)  
    db.session.add(user)
    db.session.commit()
    
    return user

def get_role_by_name(role_name):
    """Retorna el rol con el nombre especificado"""
    return Role.query.filter_by(name=role_name).first()

def find_user_by_email(email):
    """Busca un usuario por su dirección de correo electrónico"""
    return User.query.filter_by(email=email).first()

def find_user_by_id(user_id):
    """Busca un usuario por su ID"""
    return User.query.get(user_id)

def check_user(email, password):
    """Verifica las credenciales del usuario"""
    user = find_user_by_email(email)

    if user and bcrypt.check_password_hash(user.password, password):
        # Almacenar el ID del usuario en la sesion para utilizarlo en el front
        session['user_id'] = user.id
        #print(f"Usuario autenticado: {user.email}, id: {user.id}")
        return user
    
    return None

def create_permission(name):
    """Crea un nuevo permiso en la base de datos"""
    if not get_permission_by_name(name):
        permission = Permission(name=name)
        db.session.add(permission)
        db.session.commit()
        return permission
    return get_permission_by_name(name)

def create_role(name):
    """Crea un nuevo rol en la base de datos"""
    if not get_role_by_name(name):
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
        return role
    return get_role_by_name(name)

def get_permission_by_name(name):
    """Retorna un permiso basado en su nombre."""
    return Permission.query.filter_by(name=name).first()

def assign_permission_to_role(role, permission):
    """Asigna un permiso a un rol."""
    if permission not in role.permissions:
        role.permissions.append(permission)
        db.session.commit()

def initialize_roles_and_permissions():
    """Inicializa los roles y permisos en la base de datos."""
    for role_name in ROLE_PERMISSIONS.keys():
        create_role(role_name)
        
    for permission_name in PERMISSIONS:
        create_permission(permission_name)
        
    for role_name, perms in ROLE_PERMISSIONS.items():
        role = get_role_by_name(role_name)
        for perm_name in perms:
            perm = get_permission_by_name(perm_name)
            assign_permission_to_role(role, perm)
            
def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    user_id = session.get('user_id')
    
    return find_user_by_id(user_id) if user_id else None

def update_user_profile(user, alias, email):
    """Actualiza el perfil de un usuario"""
    
    # Validar si hubo cambios
    if user.alias == alias and user.email == email:
        raise ValueError("No se realizaron cambios en el perfil.")
    
    # Verificar si el email es único
    if user.email != email:
        existing_user = find_user_by_email(email)
        if existing_user:
            raise ValueError("El email ya está registrado. Elija otro email.")
    
    # Actualizar los datos del usuario
    user.alias = alias
    user.email = email
    user.updated_at = db.func.now()
    
    db.session.commit()

def toggle_block_status(target_user_id, action):
    """
    Bloquea o bloquea a un usuario dependiendo de la acción solicitada. No se puede bloquear a un System Admin.
    
    Parámetros:
    - target_user_id: El ID del usuario objetivo al que se le aplicará la acción.
    - action: La acción solicitada ('block' o 'unblock').

    Retorna un mensaje de éxito o error dependiendo del resultado.
    """
    target_user = find_user_by_id(target_user_id)
    
    if not target_user:
        return {'status': 'error', 'message': 'Usuario no encontrado.'}

    if is_system_admin(target_user):
        return {'status': 'error', 'message': 'No se puede bloquear a un System Admin.'}
    
    if action == 'block' and target_user.active:
        target_user.active = False
        db.session.commit()
        return {'status': 'success', 'message': f'El usuario {target_user.alias} ha sido bloqueado.'}
    elif action == 'unblock' and not target_user.active:
        target_user.active = True
        db.session.commit()
        return {'status': 'success', 'message': f'El usuario {target_user.alias} ha sido desbloqueado.'}
    else:
        return {'status': 'error', 'message': 'Acción inválida o el estado del usuario no permite esta acción.'}


def change_rol(user, new_role):
    """
    Cambia el rol de un usuario.
    
    Parámetros:
    - user: Usuario cuyo rol se cambiará.
    - new_role: El nombre del nuevo rol que se asignará.

    Retorna un mensaje de éxito o error dependiendo del resultado.
    """
    
    if not user:
        return {"status": "error", "message": "Usuario no encontrado."}
    
    if is_system_admin(user):
        return {"status": "error", "message": "No se puede cambiar el rol del system admin."}

    role = get_role_by_name(new_role)
    if user.role == role:
        return {"status": "warning", "message": "Se seleccionó el mismo rol que ya tiene el usuario."}
    
    user.role = role
    db.session.commit()
    return {"status": "success", "message": f"Rol de {user.alias} actualizado correctamente."}

def delete_user(user_id):
    """Realiza un eliminado lógico de un usuario."""
    user = User.query.get(user_id)
    
    if not user:
        raise ValueError("Usuario no encontrado.")
    
    if user.is_deleted:
        raise ValueError("El usuario ya está eliminado.")
    
    user.is_deleted = True
    db.session.commit()
    
    return user

def change_is_deleted(user_id):
    """Cambia el estado de is_deleted a False para recuperar el usuario de un empleado"""
    user = User.query.get(user_id)

    if not user:
        raise ValueError("Usuario no encontrado")
    
    user.is_deleted = False
    user.inserted_at = db.func.now()
    user.updated_at = user.inserted_at
    db.session.commit()
    return user

def change_password(psswd1, psswd2, psswd3):
    """Cambia la contraseña del usuario actual."""
    user = get_current_user()
    
    if not bcrypt.check_password_hash(user.password, psswd1):
        raise ValueError("Contraseña actual incorrecta.")
    
    if psswd2 != psswd3:
        raise ValueError("No coincide la nueva contraseña.")
    
    if psswd1 == psswd2:
        raise ValueError("La nueva contraseña no puede ser igual a la actual.")
    
    hashed_new_password = bcrypt.generate_password_hash(psswd2.encode('utf-8')).decode('utf-8')
    user.password = hashed_new_password
    db.session.commit()

def sa_change_password(psswd1, psswd2, psswd3, user):
    """Cambia la contraseña de un usuario siendo System Admin"""
    userSA = get_current_user()
    
    if not bcrypt.check_password_hash(userSA.password, psswd1):
        raise ValueError("Contraseña actual incorrecta.")
    
    if psswd2 != psswd3:
        raise ValueError("No coincide la nueva contraseña para el usuario.")
    
    if bcrypt.check_password_hash(user.password, psswd2):
        raise ValueError("La nueva contraseña no puede ser igual a la actual para el usuario.")
    
    hashed_new_password = bcrypt.generate_password_hash(psswd2.encode('utf-8')).decode('utf-8')
    user.password = hashed_new_password
    db.session.commit()

