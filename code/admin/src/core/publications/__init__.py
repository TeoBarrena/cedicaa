from src.core.publications.publication import Publication
from src.core.database import db
from datetime import datetime

def create_publication(**kwargs):
    """Crea una publicacion y lo guarda en la base de datos"""
    publication = Publication(**kwargs)

    try:
        db.session.add(publication)
        db.session.commit()
        return publication
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error

def list_publications(page, per_page, order='asc', status_filter=None):
    """Realiza un filtrado por is_deleted en False y devuelve una lista de todas las publicaciones que cumplen esta condición"""
    query = Publication.query.filter_by(is_deleted=False)

    if status_filter:
        query = query.filter(Publication.status == status_filter)
    
    if order == 'asc':
        query = query.order_by(Publication.creation_date.asc())
    else:
        query = query.order_by(Publication.creation_date.desc())

    # Retornar la paginación
    return query.paginate(page=page, per_page=per_page, error_out=False)

def find_publication_by_id(publication_id):
    """Busca una publicación por su ID"""
    return Publication.query.get(publication_id)

def destroy_publication(publication_id):
    """Elimina lógicamente una publicacion de la base de datos"""
    payment_record = find_publication_by_id(publication_id)

    if not payment_record:
        raise ValueError("Registro de pago no encontrado")
    
    if payment_record.is_deleted:
        raise ValueError("El empleado ya estaba eliminado")
    
    payment_record.is_deleted = True

    db.session.commit()
    return payment_record

def has_not_changes(publication, updated_data):
    """Verifica si hay cambios en los datos de la publicación registrada."""

    # Verificar si cada campo tiene el mismo valor que en la base de datos
    return (str(publication.title) == updated_data.get('title') and
            str(publication.summary) == updated_data.get('summary') and
            str(publication.content) == updated_data.get('content') and
            str(publication.status) == updated_data.get('status') and
            str(publication.author_id) == updated_data.get('author_id'))

def update_publication(publication, updated_data):
    """Actualiza la información de una publicación existente."""

    # Verificar si hay cambios
    if has_not_changes(publication, updated_data):
        raise ValueError("No se realizaron cambios en la publicación.")

    # Actualizar los datos
    for key, value in updated_data.items():
        setattr(publication, key, value)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error

def publish_publication(publication):
    publication.status = "Publicado"
    publication.publication_date = datetime.now()
    db.session.commit()

def archive_publication(publication):
    publication.status = "Archivado"
    db.session.commit()