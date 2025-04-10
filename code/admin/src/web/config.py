from os import environ

class Config(object):
    """Configuración base"""
    
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    """Configuracion para producción"""
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }
    CORS_ALLOWED_ORIGINS = [
        "https://grupo35.proyecto2024.linti.unlp.edu.ar",  # Dominio de producción
        "http://localhost:4173"  # Para pruebas locales
    ]

class DevelopmentConfig(Config):
    """Configuracion para desarrollo"""
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "eCAgaP6PLEczxjgD9G3h"
    MINIO_SECRET_KEY = "qSCCfw7XndQ0hReMPQ4w2cp5TFkxUmkEwpNE7H5l"
    MINIO_SECURE = False
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo35"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]


class TestingConfig(Config):
    """Configuracion para testing"""
    
    TESTING = True    


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}