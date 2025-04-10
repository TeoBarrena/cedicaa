from src.core.payment_record.payment_record import PaymentRecord
from src.core.database import db

def list_payments(page, per_page, order='asc', payment_type='', start_date=None, end_date=None):
    """Realiza un flitrado por is_deleted en False y devuelve una lista de todos los registros de pagos que cumplen esta condición"""
    
    query = PaymentRecord.query.filter_by(is_deleted=False)

    # Filtrar por payment_type
    if payment_type:
        query = query.filter(PaymentRecord.payment_type == payment_type)

    # Filtrar por rango de fechas
    if start_date:
        query = query.filter(PaymentRecord.payment_date >= start_date)
    if end_date:
        query = query.filter(PaymentRecord.payment_date <= end_date)

    # Aplicar ordenación
    if order == 'asc':
        query = query.order_by(PaymentRecord.payment_date.asc())
    else: 
        query = query.order_by(PaymentRecord.payment_date.desc())

    # Retornar la paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_payment_record(new_data):
    """Crea un registro de pago y lo guarda en la base de datos"""
    payment = PaymentRecord(**new_data)

    try:
        db.session.add(payment)
        db.session.commit()
        return payment
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error

def find_payment_record_by_id(payment_record_id):
    """Busca un registro de pago por su ID"""
    return PaymentRecord.query.get(payment_record_id)

def destroy_payment_record(payment_record_id):
    """Elimina lógicamente un registro de pago de la base de datos"""
    payment_record = find_payment_record_by_id(payment_record_id)

    if not payment_record:
        raise ValueError("Registro de pago no encontrado")
    
    if payment_record.is_deleted:
        raise ValueError("El empleado ya estaba eliminado")
    
    payment_record.is_deleted = True

    db.session.commit()
    return payment_record

def has_not_changes(payment_record, updated_data):
    """Verifica si hay cambios en los datos del pago registrado."""

    if updated_data.get('payment_type') != 'Honorarios':
        payment_record.employee_id = None

    # Retornar el resultado final
    return (str(payment_record.payment_date) == updated_data.get('payment_date') and
            str(payment_record.amount) == str(updated_data.get('amount')) and
            str(payment_record.payment_type) == updated_data.get('payment_type') and
            payment_record.description == updated_data.get('description') and
            str(payment_record.employee_id) == updated_data.get('employee_id'))



def update_payment_record(payment, updated_data):
    """Actualiza la información de un empleado existente."""

    # Verificar si hay cambios
    if has_not_changes(payment, updated_data):
        raise ValueError("No se realizaron cambios en el perfil.")

    # Actualizar los datos
    for key, value in updated_data.items():
        setattr(payment, key, value)

    try:
        db.session.commit()
        return True, "Registro de pago actualizado correctamente"
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        return False, f"Error al actualizar el registro de pago: {str(e)}"