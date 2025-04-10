from flask import render_template, redirect, url_for
from flask import Blueprint, request, flash
from src.core import auth
from src.core.database import db
from src.web.handlers.auth import check
from src.core.auth import get_current_user, toggle_block_status, delete_user
from src.core.auth import find_user_by_id, create_user, update_user_profile, change_rol
from src.core.employees import list_employee_not_user, find_employee_by_id
from src.core.auth.utils import ROLE_TRANSLATIONS


bp = Blueprint("users", __name__, url_prefix="/usuarios")

@bp.route("/", methods=["GET", "POST"])
@check("user_index")
def index():

    # Inicializar variables para la paginación y los filtros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    email = request.args.get('email', '', type=str)
    active = request.args.get('active')
    role = request.args.get('role', '', type=str)
    sort_by = request.args.get('sort_by', 'email', type=str)
    order = request.args.get('order', 'asc', type=str)

    # Convertir el valor del estado activo a booleano si está presente
    active_filter = None
    if active == '1':
        active_filter = True
    elif active == '0':
        active_filter = False

    # Obtener la lista de usuarios con paginación y filtros
    users_pagination = auth.list_users(page, per_page, email=email, active=active_filter, role=role, 
        sort_by=sort_by, order=order)

    # Obtener la acción de bloqueo/desbloqueo si existe
    action = request.args.get('action')
    user_id = request.args.get('user_id')

    # Manejar acción de bloqueo/desbloqueo
    if action in ["block", "unblock"] and user_id:
        result = toggle_user_block_status(user_id, action)
        flash(result['message'], 'success' if result['status'] == 'success' else 'error')

    # Si es una petición POST, se maneja el cambio de rol
    if request.method == "POST":
        new_role = request.form.get("new_role")
        user_id = request.form.get("user_id")

        user = find_user_by_id(user_id)
        role_change_result = change_user_role(user, new_role)

        flash(role_change_result['message'], 'success' if role_change_result['status'] == 'success' else 'error')
        return redirect(url_for('users.index', 
                            page=request.form.get('page', 1), 
                            per_page=request.form.get('per_page', 10), 
                            email=request.form.get('email', ''), 
                            active=request.form.get('active', ''), 
                            role=request.form.get('role', ''), 
                            sort_by=request.form.get('sort_by', 'email'), 
                            order=request.form.get('order', 'asc')))

    # Renderizar la plantilla con los usuarios paginados y los filtros
    return render_template("users/index.html", users_pagination=users_pagination, per_page=per_page, 
        email=email, active=active, role=role, sort_by=sort_by, order=order, roles=ROLE_TRANSLATIONS)

@bp.route("/nuevo", methods=["GET", "POST"])
@check("user_new")
def new():
    employees = list_employee_not_user()
    if not employees:
                flash("No hay empleados disponibles sin usuario en el sistema.", "error")
                return redirect(url_for("users.index"))
    
    employee_id = request.args.get("employee_id")
    preselected_employee = None
    
    if employee_id:
        preselected_employee = find_employee_by_id(employee_id)
        
        if not preselected_employee or preselected_employee.user:
            flash("El empleado no existe o ya tiene usuario.", "error")
            return redirect(url_for("users.index"))
    
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        email = request.form.get("email")
        password = request.form.get("password")
        alias = request.form.get("alias")
        role_name = request.form.get("role")  

        if not email or not password or not alias or not role_name or not employee_id:
            flash("Todos los campos son obligatorios.", "error")
            return render_template("users/new.html", roles=ROLE_TRANSLATIONS, employees=employees, preselected_employee=preselected_employee)

        try:
            user = create_user(email=email, password=password, alias=alias, role=role_name, employee_id=employee_id)
            flash(f"Usuario {user.alias} creado exitosamente.", "success")
            return redirect(url_for("users.sa_user_show", user_id=user.id))
        except ValueError as ve:
            flash(str(ve), "error")
            preselected_employee = find_employee_by_id(employee_id)
            return render_template("users/new.html", roles=ROLE_TRANSLATIONS, employees=employees, preselected_employee=preselected_employee)
        except Exception as e:
            flash(f"Error al crear el usuario: {str(e)}", "error")
            return render_template("users/new.html", roles=ROLE_TRANSLATIONS, employees=employees, preselected_employee=preselected_employee)

    # Método GET: mostrar formulario vacío
    return render_template("users/new.html", roles=ROLE_TRANSLATIONS, employees=employees, preselected_employee=preselected_employee)

@bp.route("/eliminar/<int:user_id>", methods=["POST"])
@check("user_destroy")
def destroy(user_id):
    try:
        user = delete_user(user_id)
        flash(f"Usuario {user.alias} eliminado exitosamente.", "success")
        return redirect(url_for("users.index"))  
    except ValueError as ve:
        flash(str(ve), "error")
        return redirect(url_for("users.index"))  
    except Exception as e:
        flash(f"Error al eliminar el usuario: {str(e)}", "error")
        return redirect(url_for("users.index"))

@bp.route("/perfil/editar", methods=["GET", "POST"])
@check("user_update")
def update():
    user = get_current_user()
    
    if user.is_deleted:
        flash("El usuario ha sido eliminado.", "error")
        return redirect(url_for("users.index")) 
    
    if request.method == "POST":
        alias = request.form.get("alias")
        email = request.form.get("email")
        
        if not alias or not email:
            flash("Todos los campos son obligatorios.", "warning")
            return render_template('users/edit_profile.html', user=user)
        
        try:
            update_user_profile(user, alias, email)
            flash(f"Perfil actualizado correctamente.", "success")
            return redirect(url_for('users.show'))
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            flash(f"Error al actualizar el perfil: {str(e)}", "error")
    
    return render_template("users/edit_profile.html", user=user)

@bp.route("/perfil/editar/<int:user_id>", methods=["GET", "POST"])
@check("sa_user_update")
def sa_update(user_id):
    user = find_user_by_id(user_id)
    
    if user.is_deleted:
        flash("El usuario ha sido eliminado.", "error")
        return redirect(url_for("users.index")) 
    
    if request.method == "POST":
        alias = request.form.get("alias")
        email = request.form.get("email")
        
        if not alias or not email:
            flash("Todos los campos son obligatorios.", "warning")
            return render_template('users/edit_profile.html', user=user)
        
        try:
            update_user_profile(user, alias, email)
            flash(f"Perfil actualizado correctamente.", "success")
            return redirect(url_for('users.sa_user_show', user_id=user.id))
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            flash(f"Error al actualizar el perfil: {str(e)}", "error")
    
    return render_template("users/admin_edit_profile.html", user=user, roles=ROLE_TRANSLATIONS)

@bp.get("/perfil")
@check("user_show")
def show():
    user = get_current_user()
    
    if user.is_deleted:
        flash("El usuario ha sido eliminado.", "error")
        return redirect(url_for("users.index"))  
    
    return render_template("users/profile.html", user=user)

@bp.route("/perfil_usuario/<int:user_id>", methods=["GET", "POST"])
@check("sa_user_show")
def sa_user_show(user_id):
    user = find_user_by_id(user_id)
    
    if user.is_deleted:
        flash("El usuario ha sido eliminado.", "error")
        return redirect(url_for("users.index"))
    
    if request.method == "POST":
        action = request.form.get('action')
        
        if action in ['block', 'unblock']:
            result = toggle_user_block_status(user_id, action)
            flash(result['message'], 'success' if result['status'] == 'success' else 'error')

        elif action == 'change_role':
            new_role = request.form.get("new_role")
            result = change_user_role(user, new_role)
            flash(result['message'], 'success' if result['status'] == 'success' else 'error')
    
    return render_template('users/admin_user_profile.html', user=user, roles=ROLE_TRANSLATIONS)

@check("block_user")
def toggle_user_block_status(target_user_id, action):
    
    return toggle_block_status(target_user_id, action)

@check("change_role")
def change_user_role(user, new_role):
    
    return change_rol(user, new_role)