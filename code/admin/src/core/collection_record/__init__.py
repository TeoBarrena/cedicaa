from src.core.collection_record.collection_record import CollectionRecord
from src.core.database import db
from src.core.employees import Employee
from src.core.jinete_amazonas import Rider
from datetime import datetime
from sqlalchemy import func

def get_collection_record(page, per_page, rider_first_name=None, rider_last_name=None, payment_method=None,
                            received_by_first_name=None, received_by_last_name=None,
                            start_date=None, end_date=None, sort_order='desc'):
    """Retorna todas los cobros"""
    
    # Empezamos la consulta desde CollectionRecord
    collection_record = CollectionRecord.query.filter(CollectionRecord.is_deleted == False)

    # Realizamos el join explícito con Rider
    collection_record = collection_record.join(Rider, CollectionRecord.rider_id == Rider.id)

    # Filtrar por nombre y apellido del jinete o amazona
    if rider_first_name:
        collection_record = collection_record.filter(Rider.first_name.ilike(f'%{rider_first_name}%'))
    
    if rider_last_name:
        collection_record = collection_record.filter(Rider.last_name.ilike(f'%{rider_last_name}%'))
    
    # Filtros por rango de fecha
    if start_date and end_date:
        collection_record = collection_record.filter(CollectionRecord.payment_date.between(start_date, end_date))
    
    # Filtro por medio de pago en CollectionRecord
    if payment_method:
        collection_record = collection_record.filter(CollectionRecord.payment_method == payment_method)
    
    # Filtro por nombre y apellido de quien recibe el pago (Employee)
    if received_by_first_name or received_by_last_name:
        collection_record = collection_record.join(Employee, CollectionRecord.received_by_id == Employee.id)
        
        if received_by_first_name:
            collection_record = collection_record.filter(Employee.name.ilike(f'%{received_by_first_name}%'))
        
        if received_by_last_name:
            collection_record = collection_record.filter(Employee.lastname.ilike(f'%{received_by_last_name}%'))
    
    # Ordenar resultados
    if sort_order == 'asc':
        collection_record = collection_record.order_by(CollectionRecord.payment_date.asc())
    else:
        collection_record = collection_record.order_by(CollectionRecord.payment_date.desc())

    return collection_record.paginate(page=page, per_page=per_page, error_out=False)



def create_new_collection(**kwargs):
    """Crea un nuevo Cobro en la base de datos """

    collection = CollectionRecord(**kwargs)
    db.session.add(collection)
    db.session.commit()
    
    return collection

def get_collection_record_by_id(collection_id):
    return CollectionRecord.query.get(collection_id)

def uptodate(collection_record, notes, payment_method, received_by_id):

    if collection_record:
        collection_record.is_pay = True
        collection_record.payment_date = datetime.now()
        if (notes):
            collection_record.notes = notes
        collection_record.payment_method = payment_method
        collection_record.received_by_id = received_by_id
        db.session.commit() 

    return collection_record


def detroy_collection(collection_record):
    """Elimina un cobro de la base de datos"""

    if not collection_record:
        raise ValueError("Cobro no encontrado")
    
    if collection_record.is_deleted:
        raise ValueError("Este cobro ya estaba eliminado")
    
    collection_record.is_deleted = True

    db.session.commit()
    return collection_record

def get_between_dates(start_date, end_date):
    """
    Obtiene los registros de cobro entre dos fechas, agrupados por mes y año, 
    solo con la fecha de pago y el monto total del mes.
    """
    query = (db.session.query(
                func.extract('year', CollectionRecord.payment_date).label('year'),
                func.extract('month', CollectionRecord.payment_date).label('month'),
                func.sum(CollectionRecord.amount).label('monthly_income')
            )
            .filter(CollectionRecord.is_pay == True)
            .filter(CollectionRecord.is_deleted == False)
            .filter(CollectionRecord.payment_date != None)
            .filter(CollectionRecord.payment_date.between(start_date, end_date))
            .group_by(func.extract('year', CollectionRecord.payment_date),
                        func.extract('month', CollectionRecord.payment_date))
            .order_by(func.extract('year', CollectionRecord.payment_date),
                        func.extract('month', CollectionRecord.payment_date))
            .all())
    
    return query


def get_debtor_riders(page, per_page):
    """
    Obtiene los jinetes que tienen deudas pendientes ordenados alfabéticamente por apellido.
    """
    query = (db.session.query(Rider.first_name, Rider.last_name,
            func.sum(CollectionRecord.amount).label('total_due'))
            .join(CollectionRecord, CollectionRecord.rider_id == Rider.id)
            .filter(Rider.is_deleted == False, CollectionRecord.is_deleted == False, CollectionRecord.is_pay == False)
            .group_by(Rider.id)
            .order_by(Rider.last_name))
    
    return query.paginate(page=page, per_page=per_page, error_out=False)
