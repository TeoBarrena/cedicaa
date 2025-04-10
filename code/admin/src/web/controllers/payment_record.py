from flask import render_template, redirect, url_for
from flask import Blueprint, request, flash
from src.web.handlers.auth import check
from src.core.payment_record import list_payments, create_payment_record, find_payment_record_by_id, destroy_payment_record, update_payment_record
from datetime import datetime
from src.core.employees import get_employees_not_deleteds
from src.core.payment_record.utils import PAYMENTS_TYPES

bp = Blueprint("payments_record", __name__, url_prefix="/payments_record")

#falta poder ordenar por estos
"""Rango de fechas de pago.
Tipo de pago: Honorarios | proveedor | gastos vario"""

@bp.get("/") 
@check("payments_index")
def index():
    today = datetime.now().date()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order = request.args.get('order', 'asc', type=str)
    
    payment_type = request.args.get('payment_type', '')
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)

    payments_pagination = list_payments(page, per_page, order=order,payment_type=payment_type, 
                                         start_date=start_date, 
                                         end_date=end_date)

    return render_template("payment_record/index.html", payments_pagination=payments_pagination, per_page=per_page, 
                        order=order, today=today, payments_types = PAYMENTS_TYPES)


@bp.route("/nuevo", methods=["GET","POST"]) 
@check("payments_create")
def create():
    today = datetime.now().date()

    employees = get_employees_not_deleteds()
    
    if request.method == "POST":
        new_payment = request.form.copy()
        try:
            create_payment_record(new_payment)
            flash(f"Pago registrado éxitosamente")
            return redirect(url_for("payments_record.index")) 
        except ValueError as e:
            flash(f"Error al registrar el pago {str(e)}")

    return render_template("payment_record/new.html", today=today, employees = employees)

@bp.route("/eliminar_payment/<int:payment_record_id>", methods=["POST"])
@check("employee_destroy")
def destroy(payment_record_id):
    try:
        payment_record = destroy_payment_record(payment_record_id)
        flash(f"Registro de pago {payment_record.id} eliminado éxitosamente.", "success")
        return redirect(url_for("payments_record.index"))
    except ValueError as ve:
        flash(str(ve), "error")
        return redirect(url_for("payments_record.index"))
    except Exception as e:
        flash(f"Error al eliminar el registro de pago: {str(e)}", "error")
        return redirect(url_for("payments_record.index"))

@bp.route("/update_payment/<int:payment_record_id>", methods=["GET", "POST"])
@check("payments_update")
def update(payment_record_id):
    today = datetime.now().date()
    payment_record = find_payment_record_by_id(payment_record_id)

    employees = get_employees_not_deleteds()

    if not payment_record:
        flash("Registro de pago no encontrado.", "error")
        return redirect(url_for("payments_record.index"))
    
    if request.method == "POST":
        updated_data = request.form.copy()

        try:
            update_payment_record(payment_record,updated_data)
            flash(f"Registro de pago modificado con éxito")
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            flash(f"Error al actualizar el pago registrado: {str(e)}", "error")
    
    return render_template("payment_record/edit_payment_record.html", payment_record = payment_record, payments_types = PAYMENTS_TYPES , today=today, employees = employees)


@bp.route("/payment/<int:payment_record_id>", methods=["GET","POST"]) 
@check("payments_show")
def show(payment_record_id):

    payment_record = find_payment_record_by_id(payment_record_id)

    if not payment_record:
        flash("Registro de pago no encontrado.", "error")
        return redirect(url_for("payments_record.index"))
                
    return render_template("payment_record/show.html", payment_record = payment_record)
