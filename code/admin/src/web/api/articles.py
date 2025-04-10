from flask import Blueprint, request, jsonify
from src.web.handlers.json import handle_bad_json
from datetime import datetime
from src.core.publications import Publication
from src.web.schemas.article import ArticleListSchema


bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")

@bp.get("/")
def index():

    author = request.args.get('author')  # "María García"
    published_from = request.args.get('published_from')  # "2023-10-10T01:00:00Z"
    published_to = request.args.get('published_to')  # "2023-10-10T12:00:00Z"
    page = request.args.get('page', default=1, type=int)  # 1
    per_page = request.args.get('per_page', default=5, type=int)  # 5
    title = request.args.get('title') 

    if published_from:
        published_from = datetime.fromisoformat(published_from.replace('Z', '+00:00'))
    if published_to:
        published_to = datetime.fromisoformat(published_to.replace('Z', '+00:00'))

    query = Publication.query.filter(Publication.status == 'Publicado', Publication.is_deleted == False).order_by(Publication.publication_date.desc())

    if title:
        query = query.filter(Publication.title == title)

    if author:
        query = query.filter(Publication.author == author)
    
    if published_from:
        query = query.filter(Publication.publication_date >= published_from)
    if published_to:
        query = query.filter(Publication.publication_date <= published_to)
    
    publications_query = query.paginate(page=page, per_page=per_page, error_out=False)

    #serializar la respuesta
    article_list_schema = ArticleListSchema()
    response_data = {
        "data": publications_query.items,
        "page": publications_query.page,
        "per_page": publications_query.per_page,
        "total": publications_query.total,
    }

    response_json = article_list_schema.dump(response_data)

    return jsonify(response_json), 200
