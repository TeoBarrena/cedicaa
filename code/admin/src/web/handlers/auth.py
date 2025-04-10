from functools import wraps
from flask import render_template
from flask import session, abort
from src.core import auth

def is_authenticated(session):
    return session.get('user') is not None

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            return render_template('auth/login.html')
        return func(*args, **kwargs)
    return wrapper

def check_permission(session, permission):
    """Chequear si el usuario tiene el permiso pasado por parametro"""
    user_id = session.get('user_id')
    user = auth.find_user_by_id(user_id)
    
    if user and auth.is_system_admin(user):
        return True
    
    permissions = auth.get_permissions(user)
    print("ACA")
    print(f"User: {user}, Permissions: {permissions}")
    
    return user is not None and permission in permissions

def check(permission):
    
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if not check_permission(session, permission):
                return abort(403)
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator