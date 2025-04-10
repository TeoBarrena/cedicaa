from src.web.handlers.auth import check
from flask import Blueprint, render_template, request, flash, url_for, redirect
from src.core.collection_record import get_collection_record, get_collection_record_by_id, uptodate, detroy_collection, create_new_collection
from datetime import datetime
from src.core.jinete_amazonas import get_riders_not_deleteds
from src.core.employees import get_employees_not_deleteds

bp = Blueprint("collection_record", __name__, url_prefix="/collection_record")

@bp.route('/', methods=['GET'])
@check("collection_index")
def index():
    rider_first_name = request.args.get('rider_first_name')
    rider_last_name = request.args.get('rider_last_name')
    payment_method = request.args.get('payment_method')
    received_by_first_name = request.args.get('received_by_first_name')
    received_by_last_name = request.args.get('received_by_last_name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_order = request.args.get('sort_order', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    pagination = get_collection_record(page, per_page, rider_first_name, rider_last_name, payment_method, received_by_first_name, received_by_last_name, start_date, end_date,sort_order)
    
    collection = pagination.items
    
    return render_template('collection_record/index.html', collection=collection, pagination=pagination, per_page=per_page)



@bp.route('/up_to_date/<int:collection_id>', methods=['GET', 'POST'])
@check("collection_update")
def up_to_date(collection_id):
    """Marca como al día el pago de un jinete o amazona"""
    collection_record = get_collection_record_by_id(collection_id)

    if request.method == 'POST':
        # Captura los datos enviados por el formulario
        notes = request.form.get('notes', '')
        payment_method = request.form.get('payment_method')
        if payment_method == "OTRO":
            payment_method = request.form.get('other_payment_method')
        received_by_id = request.form.get('received_by_id')

        # Actualiza el registro de cobro
        if uptodate(collection_record, notes, payment_method, received_by_id):
            flash('El jinete o amazona está al día con los pagos.', 'success')
        else:
            flash('No se encontró el registro del cobro.', 'danger')

        return redirect(url_for('collection_record.index'))

    # Si es GET, mostrar el formulario de pago
    employees = get_employees_not_deleteds()  # Asume que tienes una función para obtener todos los empleados
    return render_template('collection_record/pay.html', collection_record=collection_record, employees=employees)


@bp.route('/destroy/<int:collection_id>', methods=['POST'])
@check("collection_destroy")
def destroy(collection_id):
    """Eliminacion de pago de un jinete o amazona"""
    collection_record = get_collection_record_by_id(collection_id)

    try:
        collection_record = detroy_collection(collection_record)
        flash(f"Cobro  eliminado éxitosamente.", "success")
        return redirect(url_for("collection_record.index"))
    except ValueError as ve:
        flash(str(ve), "error")
        return redirect(url_for("collection_record.index"))
    except Exception as e:
        flash(f"Error al eliminar el pago: {str(e)}", "error")
        return redirect(url_for("collection_record.index"))
    
@bp.route('/create', methods=["GET", "POST"])
@check("collection_create")
def create():
    riders = get_riders_not_deleteds().all()
    employees = get_employees_not_deleteds().all()

    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            rider_id = request.form.get('rider_id')
            amount = float(request.form.get('amount'))
            notes = request.form.get('notes', '')
            is_pay = True if request.form.get('is_pay') == 'True' else False
            payment_method = request.form.get('payment_method')
            if (payment_method == "OTRO"):
                payment_method = request.form.get('other_payment_method')
            received_by_id = request.form.get('received_by_id')
            
            # Crear un nuevo registro de pago
            new_record = create_new_collection(
                rider_id=rider_id,
                payment_date=datetime.now(),
                payment_method=payment_method,
                amount=amount,
                received_by_id=received_by_id,
                notes=notes,
                is_pay=is_pay
            )
            
            # Mensaje de éxito
            flash('Registro de pago creado exitosamente.', 'success')
            return redirect(url_for('collection_record.index'))
        except Exception as e:
            # Mensaje de error en caso de fallo
            flash(f'Error al crear el registro de pago: {str(e)}', 'danger')
            return redirect(url_for('collection_record.create'))

    # Renderizar el formulario de creación
    return render_template('collection_record/create.html', riders=riders, employees=employees)