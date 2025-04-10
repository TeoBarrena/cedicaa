from flask import Blueprint, request, render_template
from flask import flash, redirect, url_for
from src.web.handlers.auth import check
from src.core import messages
from src.core.messages.utils import STATES_TRANSLATIONS

bp = Blueprint("messages", __name__, url_prefix="/consultas")

@bp.route("/", methods=["GET", "POST"])
@check("contact_index")
def index():
    
    # Parámetros de paginación
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Filtros
    email = request.args.get('email', '', type=str)
    state = request.args.get('state', '', type=str) 
    sort_by = request.args.get('sort_by', 'inserted_at', type=str)
    order = request.args.get('order', 'desc', type=str)

    messages_pagination = messages.list_messages(page, per_page,email=email, state=state, sort_by=sort_by, order=order)
    
    return render_template("messages/index.html", messages_pagination=messages_pagination, per_page=per_page,
        state=state, sort_by=sort_by, order=order, states_translations=STATES_TRANSLATIONS
    )

@bp.get("/show/<int:id_message>")
@check("contact_show")
def show(id_message):
    message = messages.find_message_by_id(id_message)
    if message.is_deleted:
        flash("El mensaje ha sido eliminado.", "error")
        return redirect(url_for("messages.index"))
    
    return render_template("messages/show.html", message=message, states_translations=STATES_TRANSLATIONS)

@bp.post("/update/<int:id_message>")
@check("contact_update")
def update(id_message):
    message = messages.find_message_by_id(id_message)
    
    if not message:
        flash("El mensaje no existe.", "error")
        return redirect(url_for("messages.index"))

    if message.is_deleted:
        flash("El mensaje ha sido eliminado y no se puede modificar.", "error")
        return redirect(url_for("messages.index"))

    # Determinar la acción solicitada
    action = request.form.get("action")

    try:
        if action == "change_state":
            _change_state(message)
            flash(f"Estado de la consulta cambiado correctamente.", "success")
        elif action == "edit_comment":
            _edit_comment(message)
            flash(f"Comentario de la consulta cambiado correctamente. Comentario en estado 'Respondido'", "success")
        else:
            flash("Acción no reconocida.", "error")
    except ValueError as e:
        flash(str(e), "error")
    except Exception as e:
        flash(f"Error al actualizar la consulta: {str(e)}", "error")
    
    return redirect(url_for("messages.show", id_message=id_message))

def _change_state(message):
    """Actualiza el estado del mensaje."""
    new_state = request.form.get("state")
    messages.change_state(message, new_state)

def _edit_comment(message):
    """Actualiza el comentario del mensaje."""
    new_comment = request.form.get("comment")
    messages.edit_comment(message, new_comment) 


@bp.post("/eliminar/<int:id_message>")
@check("contact_destroy")
def destroy(id_message):
    message = messages.find_message_by_id(id_message)
    
    messages.destroy(message)
    flash ("Consulta eliminada correctamente", "success")
    
    return redirect(url_for('messages.index'))
