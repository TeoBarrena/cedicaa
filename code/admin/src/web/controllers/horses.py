from flask import render_template, redirect, url_for
from flask import Blueprint, request, flash
from datetime import datetime
from src.core import equestrian
from src.web.handlers.auth import check
from src.core import employees
from src.web.handlers.files import handle_file_upload, delete_file

bp = Blueprint("horses", __name__, url_prefix="/ecuestre")
MODULE_NAME = "equestrian"

@bp.route("/", methods=["GET", "POST"])
@check("equestrian_index")
def index():
    """ Mustra la lista de caballos con filtros y paginación """
    # Se obtienen los datos enviados del formulario
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    name = request.args.get('name', '', type=str)
    rider_type = request.args.get('rider_type', '', type=str)
    sort_by = request.args.get('sort_by', 'name', type=str)  
    order = request.args.get('order', 'asc', type=str)  
    
    horses_pagination = equestrian.list_horses(page, per_page,name=name, rider_type=rider_type, 
                                            sort_by=sort_by, order=order)
    
    return render_template("equestrian/index.html", horses_pagination=horses_pagination, per_page=per_page,name=name, 
                            rider_type=rider_type, sort_by=sort_by, order=order)

@bp.route("/crear", methods=["GET", "POST"])
@check("equestrian_create")
def create():
    """ Toma los valores del formulario para mandar a crear un nuevo caballo """
    employees_list = []
    employees_list.append(employees.get_active_trainers())
    if request.method == 'POST':
        # Toma los valores del formulario
        horse_data = get_form_data(request)
        employee_ids = request.form.getlist('employee_ids')
        if validate_dates(horse_data['birthdate'], horse_data['entry_date']):
            try:
                # Agregar el nuevo caballo a la base de datos
                new_horse = equestrian.create(**horse_data, employee_ids=employee_ids)
                flash("¡Caballo creado exitosamente!", "success")
                return render_template("equestrian/show.html", horse=new_horse, id_horse=new_horse.id)
            except Exception as e:
                flash("Error al crear el caballo: " + str(e), "error")
                return render_template('equestrian/create.html')
    return render_template('equestrian/create.html', today=get_today_date())

def get_today_date():
    """ Retorna la fecha actual en formato YYYY-MM-DD """
    return datetime.now().strftime('%Y-%m-%d')

def validate_dates(birthdate, entry_date):
    """ Valida que las fechas de nacimiento y entrada no sean futuras.
        Así como que la de entrada sea posterior a la de nacimiento."""
    current_date = datetime.strptime(get_today_date(), '%Y-%m-%d')
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    entry_date = datetime.strptime(entry_date, '%Y-%m-%d')

    if birthdate > current_date:
        flash('La fecha de nacimiento no puede ser futura.', 'error')
        return False
    elif entry_date > current_date:
        flash('La fecha de entrada no puede ser futura.', 'error')
        return False
    elif entry_date < birthdate:
        flash('La fecha de entrada no puede ser anterior a la de nacimiento.', 'error')
        return False
    return True

@bp.route("/eliminar/<int:id_horse>", methods=["GET", "POST"])
@check("equestrian_destroy")
def destroy(id_horse):
    """ Gestiona la eliminación de un caballo """
    equestrian.destroy(id_horse)
    flash ("Caballo eliminado correctamente", "success")
    return redirect(url_for('horses.index'))

@bp.route("/update/<int:id_horse>", methods=["GET", "POST"])
@check("equestrian_update")
def update(id_horse):
    """ Toma los valores del formulario para gestionar la actualización de un caballo """
    horse = equestrian.get_horse_by_id(id_horse)
    if request.method == 'POST':
        horse_data = get_form_data(request)
        employee_ids = list(map(int,request.form.getlist('employee_ids')))
        if not equestrian.is_different(horse_data, id_horse=id_horse, updated_trainer_ids=employee_ids):
            flash("No se realizaron cambios.", "warning")
            return render_template('equestrian/update.html', horse=horse, id_horse=id_horse, associated_employees=equestrian.get_employees(id_horse))
        if validate_dates(horse_data['birthdate'], horse_data['entry_date']):
            try:
                # Actualizar el caballo en la base de datos
                equestrian.update(id_horse, employee_ids,**horse_data)
                flash("¡Los datos del caballo se actualizaron exitosamente!", "success")
                return redirect(url_for('horses.show', id_horse=id_horse))
            except Exception as e:
                flash("Error al actualizar los datos del caballo: " + str(e), "danger")
                return render_template('equestrian/update.html', horse=horse, id_horse=id_horse, associated_employees=equestrian.get_employees(id_horse))
    return render_template('equestrian/update.html', horse=horse, id_horse=id_horse, associated_employees=equestrian.get_employees(id_horse))

def get_form_data(request):
    """ Obtiene los datos del formulario """
    return {
            'name': request.form['name'],
            'birthdate': request.form['birthdate'],
            'gender': request.form['gender'],
            'breed': request.form['breed'],
            'fur': request.form['fur'],
            'acquisition': request.form['acquisition'],
            'entry_date': request.form['entry_date'],
            'assigned_headquarters': request.form['assigned_headquarters'],
            'rider_type': request.form['rider_type'],
        }

@bp.route("/show/<int:id_horse>", methods=["GET"])
@check("equestrian_show")
def show(id_horse):
    horse = equestrian.show(id_horse)
    if equestrian.is_deleted(id_horse):  # Por si intentan acceder por la URL
        flash("El caballo ha sido eliminado.", "error")
        return redirect(url_for("horses.index"))
    return render_template("equestrian/show.html", horse=horse, id_horse=id_horse)


@bp.route("/files/show/<int:id_horse>", methods=["GET"])
@check("equestrian_show")
def show_files(id_horse):
    horse = equestrian.get_horse_by_id(id_horse)
    if equestrian.is_deleted(id_horse):  # Por si intentan acceder por la URL
        flash("El caballo ha sido eliminado.", "error")
        return redirect(url_for("horses.index"))
    return render_template("equestrian/show_files.html", horse=horse, id_horse=id_horse)

@bp.route("/files/update/<int:id_horse>", methods=["GET", "POST"])
@check("equestrian_update")
def update_files(id_horse):
    horse = equestrian.get_horse_by_id(id_horse)
    existing_files = get_existing_files(horse)

    if request.method == 'POST':
        horse_data = get_form_files(request)
        save_files(horse, horse_data, existing_files)
        handle_file_deletions(horse_data, request.form)
        try:
            equestrian.update_files(id_horse, **horse_data)
            flash("¡Los archivos del caballo se actualizaron exitosamente!", "success")
            return redirect(url_for('horses.show_files', id_horse=id_horse))
        except Exception as e:
            flash("Error al actualizar los archivos del caballo: " + str(e), "danger")
            return render_template('equestrian/edit_files.html', horse=horse, id_horse=id_horse)

    return render_template('equestrian/edit_files.html', horse=horse, id_horse=id_horse)

def get_existing_files(horse):
    """Obtiene los archivos existentes de un caballo"""
    return {
        'general_information': horse.general_information,
        'training_schedule': horse.training_schedule,
        'progress_report': horse.progress_report,
        'vet_records': horse.vet_records,
        'image_1': horse.image_1,
        'image_2': horse.image_2,
        'image_3': horse.image_3,
        'image_4': horse.image_4,
        'image_5': horse.image_5,
    }

def get_form_files(request):
    """Captura los archivos subidos en el formulario"""
    return {
            'general_information': request.files['general_information'],
            'training_schedule': request.files['training_schedule'],
            'progress_report': request.files['progress_report'],
            'vet_records': request.files['vet_records'],
            'image_1': request.files['image_1'],
            'image_2': request.files['image_2'],
            'image_3': request.files['image_3'],
            'image_4': request.files['image_4'],
            'image_5': request.files['image_5'],
        }

def handle_file_deletions(horse_data, request_form):
    """Eliminación de archivos según las casillas de verificación."""
    for fieldname, file_path in list(horse_data.items()):
        if f'delete_{fieldname}' in request_form:
            delete_file(file_path)
            horse_data[fieldname] = None


def save_files(horse, horse_data, existing_files):
    """Guardar los archivos subidos, o mantener los existentes si no se subió uno nuevo."""
    for key, file in list(horse_data.items()):
            if file.filename == '':
                horse_data[key] = existing_files[key]
            else:
                handle_file_upload(key, horse_data, MODULE_NAME, horse)