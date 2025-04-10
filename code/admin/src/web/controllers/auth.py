from flask import render_template
from flask import Blueprint
from flask import request
from flask import flash
from flask import session
from flask import redirect
from flask import url_for
from src.core import auth
from src.core.auth import change_password as change_psswd
from src.core.auth import sa_change_password as sa_change_psswd
from src.web.handlers.auth import login_required, check
from src.core.auth import find_user_by_id
from src.core.auth import find_user_by_email
from src.core.employees import find_employee_by_email  
from src.core.oauth_client import oauth 
from src.core.auth import create_user
from src.core.employees import asociate_user
from flask import session


import secrets

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.get("/login")
def login():
    return render_template('auth/login.html')


@bp.route('/login/google')
def login_with_google():

    nonce = secrets.token_urlsafe(16)
    session['oauth_nonce'] = nonce

    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@bp.route('/callback')
def google_callback():
    try:
        # Obtener el token de acceso
        token = oauth.google.authorize_access_token()
        
        nonce = session.pop('oauth_nonce', None)
        if not nonce:
            raise ValueError("Nonce no encontrado en la sesión")
    
        user_info = oauth.google.parse_id_token(token, nonce=nonce)

        # Procede con la verificación y sesión
        email = user_info['email']
        user = find_user_by_email(email)
        
        # Caso 1 del drive -> Si existe un usuario con ese mail registrado → Inicia sesión directamente
        if user:
            if user_deleted(user):
                flash("Usuario eliminado", "error")
                return redirect(url_for('auth.login'))
            
            if user_bloqued(user):
                flash("Usuario bloquedo", "error")
                return redirect(url_for('auth.login'))
            
            session["user"] = user.email
            session["user_id"] = user.id
            flash("Sesión iniciada correctamente con Google", "success")
            return redirect(url_for('home'))

        # Caso 2 del drive -> Si no existe un usuario con ese mail registrado
        employee = find_employee_by_email(email)
        if employee:
            # Caso 2.A -> El empleado no tiene un usuario asignado, le pregunta si quiere crear un usuario
            # Si dice q si crea el usuario en active = False y se informa que el System Admin debe habilitar el perfil
            if employee.user is None:
                session['email'] = email
                return redirect(url_for('auth.check_create_new_user',email=email))

            else:
                # Caso 2.B -> El empleado tiene un usuario asignado, inicia sesión con el mail del usuario, no con el mail del empleado
                if user_deleted(employee.user):
                    flash("Usuario eliminado", "error")
                    return redirect(url_for('auth.login'))
                
                if user_bloqued(employee.user):
                    flash("Usuario bloquedo", "error")
                    return redirect(url_for('auth.login'))
                
                session["user"] = employee.user.email
                session["user_id"] = employee.user.id
                flash("Sesión iniciada correctamente con Google", "success")
                return redirect(url_for('home'))
            
        flash("El email no está registrado en el sistema. Contacte al administrador.", "error")
        return redirect(url_for('auth.login'))
    except Exception as e:
        flash(f"Error al iniciar sesión con Google: {str(e)}", "error")
        return redirect(url_for('auth.login'))
    
@bp.route('/check_create_new_user', methods=['GET', 'POST'])
def check_create_new_user():
    email = session.get('email')
    employee = find_employee_by_email(email)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        alias = request.form.get('alias')
        if find_user_by_email(email):
            flash("Ya existe un usuario con ese email", "error")
            return redirect(url_for('auth.check_create_new_user', email=email))
        pass
        user = create_user(email=email, password=password, role_id = None, alias=alias, employee_id=employee.id, active=False)
        asociate_user(employee, user)
        flash("Usuario creado correctamente, el System Admin debe habilitar el perfil", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/check_create_new_user.html', email=email)



@bp.post("/authenticate")
def authenticate():
    params = request.form
    user = auth.check_user(params['email'], params['password'])

    if not user:
        flash("Usuario o contraseña incorrecta", "error")
        return redirect(url_for('auth.login'))
    
    if user_deleted(user):
        flash("Usuario eliminado", "error")
        return redirect(url_for('auth.login'))
    
    if user_bloqued(user):
        flash("Usuario bloquedo", "error")
        return redirect(url_for('auth.login'))
    
    session["user"] = user.email
    flash("La sesión se inició correctamente", "success")

    return redirect(url_for('home'))

@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("La sesión se cerró correctamente", "info")

    return redirect(url_for('home'))

@bp.get("/change_password")
@login_required
def change_password():
    return render_template('auth/change_password.html')

@bp.post("/modification_password")
@login_required
def modification_password():
    password1 = request.form.get("current_password")
    password2 = request.form.get("new_password")
    password3 = request.form.get("new_password_again")
    
    if not password1 or not password2 or not password3:
        flash("Todos los campos son obligatorios.", "warning")
        return render_template('auth/change_password.html')

    try:
        change_psswd(psswd1=password1, psswd2=password2, psswd3=password3)
        flash(f"Contraseña cambiada exitosamente.", "success")
        return redirect(url_for('home'))
    except ValueError as ve:
        flash(str(ve), "error")
    except Exception as e:
        flash(f"Error al cambiar la contraseña: {str(e)}", "error")
        
    return render_template('auth/change_password.html')

def user_bloqued(user):
    return user.active == False

def user_deleted(user):
    return user.is_deleted == True

@bp.get("/perfil/sa_change_password/<int:user_id>")
@check("change_password")
def sa_change_password(user_id):
    user = find_user_by_id(user_id)
    return render_template('auth/sa_change_password.html', user=user)

@bp.post("perfil/sa_modification_password/<int:user_id>")
@check("change_password")
def sa_modification_password(user_id):
    user = find_user_by_id(user_id)
    password1 = request.form.get("current_password_sa")
    password2 = request.form.get("new_password_user")
    password3 = request.form.get("new_password_again_user")
    
    if not password1 or not password2 or not password3:
        flash("Todos los campos son obligatorios.", "warning")
        return render_template('auth/sa_change_password.html', user=user)

    try:
        sa_change_psswd(psswd1=password1, psswd2=password2, psswd3=password3, user=user)
        flash(f"Contraseña del usuario cambiada exitosamente.", "success")
        return redirect(url_for('users.sa_user_show', user_id=user.id))
    except ValueError as ve:
        flash(str(ve), "error")
    except Exception as e:
        flash(f"Error al cambiar la contraseña: {str(e)}", "error")
        
    return render_template('auth/sa_change_password.html', user=user)