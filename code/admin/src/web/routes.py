from flask import render_template
from src.web.controllers.users import bp as users_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.employee_cedica import bp as employees_bp
from src.web.controllers.horses import bp as horses_bp
from src.web.controllers.payment_record import bp as payment_record_bp
from src.web.controllers.jinete_amazonas.jinete_amazonas import bp as jinete_amazonas_bp
from src.web.controllers.collection_record import bp as collection_record_bp
from src.web.controllers.data_analysis import bp as data_analysis_bp
from src.web.controllers.publications import bp as publication_bp
from src.web.controllers.messages import bp as messages_bp
from src.web.api.messages import bp as api_messages_bp
from src.web.api.articles import bp as api_articles_bp


def register(app):
    """Registro de rutas"""
    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/login")
    def login():
        return render_template("auth/login.html")
    
    
    # Registro de Blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(horses_bp)
    app.register_blueprint(payment_record_bp)
    app.register_blueprint(jinete_amazonas_bp)
    app.register_blueprint(collection_record_bp)
    app.register_blueprint(data_analysis_bp)
    app.register_blueprint(publication_bp)
    app.register_blueprint(messages_bp)
    
    # API
    app.register_blueprint(api_messages_bp)
    app.register_blueprint(api_articles_bp)

