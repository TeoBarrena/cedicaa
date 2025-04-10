from flask import current_app 

def file_url(file):
    """Obtiene la URL de un archivo en MinIO que se encuentra en el bucket 'grupo35' """
    client = current_app.storage.client
    
    if not file:
        return None
    try:
        # Verificar si el archivo existe en MinIO
        client.stat_object("grupo35", file)
        # Si el archivo existe, obtener la URL presignada
        return client.presigned_get_object("grupo35", file)
    except Exception as e:
        # Captura cualquier error si el archivo no existe o hay problemas
        current_app.logger.error(f"Error al obtener el archivo '{file}': {e}")
        return None

# La dejo por si se quiere obtener la URL de algun archivo por defecto
def default_file_url(config):
    """Obtiene la URL de un archivo por defecto"""
    protocol = "https" if config.get("MINIO_SECURE") else "http"

    print(f"default_file_url: {protocol}://{config.get("MINIO_SERVER")}/grupo35/public/file_default.png")


    return f"{protocol}://{config.get("MINIO_SERVER")}/grupo35/public/file_default.png"

