from flask import render_template, redirect, url_for
from flask import Blueprint, request, flash
from src.core import employees
from src.web.handlers.auth import check
from src.core.employees import EmailAlreadyExistsError
from src.core.employees import create_employee, find_employee_by_id,update_employee, delete_employee, save_files
from src.core.employees.utils import PROFESSION_LIST, JOB_POSITION_LIST
from src.core.jinete_amazonas.utils import PROVINCE_TOWNS
from datetime import datetime
from src.web.handlers.files import handle_file_upload

bp = Blueprint("employee_cedica", __name__, url_prefix="/employees_cedica")

@bp.get("/") 
@check("employee_index")
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    email = request.args.get('email', '', type=str)
    name = request.args.get('name', '', type=str)
    lastname = request.args.get('lastname', '', type=str)  
    dni = request.args.get('dni', '', type=str)  
    active = request.args.get('active')
    sort_by = request.args.get('sort_by', 'email', type=str)
    order = request.args.get('order', 'asc', type=str)
    job_position = request.args.get('job_position', '', type=str)  


    # Convertir el valor del estado activo a booleano si está presente
    active_filter = None
    if active == '1':
        active_filter = True
    elif active == '0':
        active_filter = False

    employees_pagination = employees.list_employees(page, per_page, email=email, name=name, lastname=lastname, dni=dni, active=active_filter, sort_by=sort_by, order=order, job_position=job_position)

    return render_template("employees_cedica/index.html", employees_pagination=employees_pagination, per_page=per_page, 
                        email=email, active=active, sort_by=sort_by, order=order, job_position=job_position, job_positions = JOB_POSITION_LIST)



@bp.route("/perfil/<int:employee_id>", methods=["GET", "POST"])
@check("employee_show")
def show(employee_id):
    employee = find_employee_by_id(employee_id)

    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employee_cedica.index"))
    
    if request.method == "POST":
        user_id = request.form.get("user_id")
        if user_id:
            try:
                from src.core.auth import change_is_deleted
                change_is_deleted(user_id)
                flash(f"Usuario recuperado éxitosamente")
            except ValueError as e:
                flash(str(e), "error")
                
    return render_template("employees_cedica/show_employee.html", employee = employee)

@bp.route("/nuevo", methods=["GET", "POST"])
@check("employee_create")
def create():
    today = datetime.now().date()

    if request.method == "POST":
        new_data = request.form.copy()
        new_data.pop("province", None)
        new_data["name"] = new_data.get("name")
        new_data["lastname"] = new_data.get("lastname")
        new_data["dni"] = new_data.get("dni")
        new_data["email"] = new_data.get("email")
        new_data["address"] = new_data.get("address")
        new_data["number"] = int(new_data.get("number"))
        new_data["departament"] = new_data.get("departament")
        new_data["town_id"] = int(new_data.get("town_id"))
        new_data["phone"] = new_data.get("phone")
        new_data["profession"] = new_data.get("profession")
        new_data["job_position"] = new_data.get("job_position")
        new_data["start_date"] = new_data.get("start_date")
        new_data["termination_date"] = new_data.get("termination_date") or None
        new_data["emergency_contact_name"] = new_data.get("emergency_contact_name")
        new_data["emergency_contact_phone"] = new_data.get("emergency_contact_phone")
        new_data["social_work"] = new_data.get("social_work")
        new_data["afilliate_number"] = new_data.get("afilliate_number")
        new_data["condition"] = new_data.get("condition")
        new_data["active"] = bool(request.form.get("active") == "on")
        new_data["title"] = None  # Asignamos None por defecto
        new_data["dni_copy"] = None  # Asignamos None por defecto
        new_data["updated_cv"] = None  # Asignamos None por defecto
        
        try:
            employee = create_employee(new_data)

            if "title" in request.files and request.files["title"].filename:  # Verifica que haya un archivo seleccionado
                handle_file_upload("title",new_data, "employee", employee )
        
            if "dni_copy" in request.files and request.files["dni_copy"].filename:
                handle_file_upload("dni_copy",new_data, "employee", employee )

            if "updated_cv" in request.files and request.files["updated_cv"].filename: 
                handle_file_upload("updated_cv",new_data, "employee", employee )

            save_files()

            flash(f"Empleado {employee.dni} creado exitosamente")
            return redirect(url_for("employee_cedica.index"))

        except EmailAlreadyExistsError as e:
            flash(str(e), "error")
            return render_template("employees_cedica/new.html", professions=PROFESSION_LIST, job_positions=JOB_POSITION_LIST, provinces=PROVINCE_TOWNS,today= today)
        except Exception as e:
            flash(f"Error al crear el empleado: {str(e)}", "error")
            return render_template("employees_cedica/new.html", professions=PROFESSION_LIST, job_positions=JOB_POSITION_LIST, provinces=PROVINCE_TOWNS,today= today)
    
    # para metodo GET
    return render_template("employees_cedica/new.html", professions=PROFESSION_LIST, job_positions=JOB_POSITION_LIST, provinces=PROVINCE_TOWNS, today= today)


@bp.route("/eliminar/<int:employee_id>", methods=["POST"])
@check("employee_destroy")
def destroy(employee_id):
    try:
        employee = delete_employee(employee_id)
        flash(f"Empleado {employee.dni} eliminado éxitosamente.", "success")
        return redirect(url_for("employee_cedica.index"))
    except ValueError as ve:
        flash(str(ve), "error")
        return redirect(url_for("employee_cedica.index"))
    except Exception as e:
        flash(f"Error al eliminar el usuario: {str(e)}", "error")
        return redirect(url_for("employee_cedica.index"))
    

@bp.route("/perfil/editar/<int:employee_id>", methods=['GET', 'POST'])
@check("employee_update")
def update(employee_id):
    today = datetime.now().date()
    employee = find_employee_by_id(employee_id)

    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employee_cedica.index"))

    if request.method == "POST":
        updated_data = request.form.copy()

        # Aquí asigna valores por defecto o actuales si son None o vacíos
        updated_data["name"] = updated_data.get("name", employee.name)
        updated_data["lastname"] = updated_data.get("lastname", employee.lastname)
        updated_data["dni"] = updated_data.get("dni", employee.dni)
        updated_data["email"] = updated_data.get("email", employee.email)
        updated_data["address"] = updated_data.get("address", employee.address)
        updated_data["number"] = int(updated_data.get("number", employee.number))
        updated_data["departament"] = updated_data.get("departament", employee.departament)
        updated_data["town_id"] = int(updated_data.get("town_id", employee.town_id))
        updated_data["phone"] = updated_data.get("phone", employee.phone)
        updated_data["profession"] = updated_data.get("profession", employee.profession)
        updated_data["job_position"] = updated_data.get("job_position", employee.job_position)
        updated_data["start_date"] = updated_data.get("start_date", employee.start_date)
        updated_data["termination_date"] = updated_data.get("termination_date", employee.termination_date)
        updated_data["emergency_contact_name"] = updated_data.get("emergency_contact_name", employee.emergency_contact_name)
        updated_data["emergency_contact_phone"] = updated_data.get("emergency_contact_phone", employee.emergency_contact_phone)
        updated_data["social_work"] = updated_data.get("social_work", employee.social_work)
        updated_data["afilliate_number"] = updated_data.get("afilliate_number", employee.afilliate_number)
        updated_data["condition"] = updated_data.get("condition", employee.condition)
        updated_data["active"] = request.form.get("active") == "on"

        if "title" in request.files and request.files["title"].filename:  # Verifica que haya un archivo seleccionado
            handle_file_upload("title",updated_data, "employee", employee )
        
        if "dni_copy" in request.files and request.files["dni_copy"].filename:
            handle_file_upload("dni_copy",updated_data, "employee", employee )

        if "updated_cv" in request.files and request.files["updated_cv"].filename: 
            handle_file_upload("updated_cv",updated_data, "employee", employee )

        try:
            update_employee(employee, updated_data)
            flash("Perfil modificado con éxito", "success")
            return redirect(url_for('employee_cedica.show', employee_id=employee.id))
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            flash(f"Error al actualizar el perfil: {str(e)}", "error")

    return render_template("employees_cedica/edit_profile.html", employee=employee, professions=PROFESSION_LIST, job_positions=JOB_POSITION_LIST, provinces=PROVINCE_TOWNS, today=today)
