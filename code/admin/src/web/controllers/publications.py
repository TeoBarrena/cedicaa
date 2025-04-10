from flask import render_template, redirect, url_for
from flask import Blueprint, request, flash
from src.web.handlers.auth import check
from src.core.publications.utils import STATES
from src.core.publications import create_publication, list_publications, destroy_publication, find_publication_by_id, update_publication, publish_publication, archive_publication
from src.core.auth import get_current_user
from datetime import datetime

bp = Blueprint("publications", __name__, url_prefix="/publications")


@bp.get("/") 
@check("editor_index")
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order = request.args.get('order', 'asc', type=str)
    status_filter = request.args.get('status_filter')

    publications_pagination = list_publications(page, per_page, order=order, status_filter=status_filter)

    
    return render_template('publications/index.html', publications=publications_pagination, states=STATES, status_filter=status_filter, per_page=per_page, page=page, order=order)


@bp.route("/create_publication", methods=["GET","POST"]) 
@check("editor_create")
def create():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        content = request.form['content']
        action = request.form['action']
        user = get_current_user()
        
        if action == "publish":
            status = "Publicado"
            publication_date = datetime.now()
            update_date = datetime.now()
        elif action == "draft":
            status = "Borrador"
            publication_date = None
            update_date = datetime.now()
        else:
            flash("Acción no reconocida.", "error")
            return redirect(url_for("publications.index"))

        new_publication = create_publication(
            title=title,
            summary=summary,
            content=content,
            author=user,
            status=status,
            publication_date=publication_date,
            update_date=update_date
        )

        if new_publication:
            flash(f'Publicación "{new_publication.title}" creada exitosamente.')
            return redirect(url_for("publications.index"))
        else:
            flash("Error al crear la publicación.", "error")
    return render_template('publications/new.html', states=STATES)


@bp.route("/destroy_publication/<int:publication_id>", methods=["POST"])
@check("editor_destroy")
def destroy(publication_id):
    try:
        publication = destroy_publication(publication_id)
        flash(f"Publicación {publication.title} eliminada éxitosamente.", "success")
        return redirect(url_for("publications.index"))
    except ValueError as ve:
        flash(str(ve), "error")
        return redirect(url_for("publications.index"))
    except Exception as e:
        flash(f"Error al eliminar el registro de pago: {str(e)}", "error")
        return redirect(url_for("publications.index"))

@bp.route("/update_publication/<int:publication_id>", methods=["GET", "POST"])
@check("editor_update")
def update(publication_id):
    publication = find_publication_by_id(publication_id)

    if not publication:
        flash("Publicación no encontrado.", "error")
        return redirect(url_for("publications.index"))
    
    if request.method == "POST":
        updated_data = request.form.copy()

        try:
            update_publication(publication,updated_data)
            flash(f"Publicacion modificada con éxito")
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            flash(f"Error al actualizar el pago registrado: {str(e)}", "error")
        
        return redirect(url_for("publications.index"))
    
    return render_template("publications/update.html", publication = publication, states=STATES)


@bp.route("/publication/<int:publication_id>", methods=["GET","POST"]) 
@check("editor_show")
def show(publication_id):

    publication = find_publication_by_id(publication_id)

    if not publication:
        flash("Registro de pago no encontrado.", "error")
        return redirect(url_for("payments_record.index"))
                
    return render_template("publications/show.html", publication = publication)

@bp.route("/publish/<int:publication_id>", methods=["POST"])
@check("editor_update")
def publish(publication_id):
    publication = find_publication_by_id(publication_id)

    if publication:
        publish_publication(publication)
        flash(f'Publicación "{publication.title}" fue publicada exitosamente.')
    else:
        flash("La publicación no se pudo publicar.", "error")

    return redirect(url_for("publications.index"))

@bp.route("/archivar/<int:publication_id>", methods=["POST"])
@check("editor_update")
def archive(publication_id):
    publication = find_publication_by_id(publication_id)

    if publication:
        archive_publication(publication)
        flash(f'Publicación "{publication.title}" fue archivada exitosamente.')
    else:
        flash("La publicación no se pudo archivar.", "error")

    return redirect(url_for("publications.index"))