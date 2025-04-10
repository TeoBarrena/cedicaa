from flask import request, flash, current_app
import io, os
import mimetypes

BUCKET_NAME = "grupo35"
ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]


def handle_file_upload(field_name, updated_data, module_name, object):
    """Maneja la subida de archivos al servidor y actualiza los datos del objeto"""
    file = request.files[field_name]
    client = current_app.storage.client

    # Verifica que el archivo tenga un nombre y tamaño
    if file and file.filename:
        try:
            file_bytes = file.read()
            file.seek(0)  # Regresa el puntero del archivo al inicio

            if not check_file_type(file):
                flash("Error: Tipo de archivo no permitido.", "error")
                return False

            file_extension = os.path.splitext(file.filename)[1]
            filename = f"{module_name}/{field_name}_{object.id}{file_extension}"
            size = len(file_bytes)
            mime_type, _ = mimetypes.guess_type(file.filename)

            if client is not None:
                client.put_object(
                    BUCKET_NAME,
                    filename,
                    io.BytesIO(file_bytes),
                    size,
                    content_type=mime_type,
                )
                updated_data[field_name] = filename
                setattr(object, field_name, filename)

                # Genera un enlace de descarga del archivo
                download_url = client.presigned_get_object(BUCKET_NAME, filename)
                updated_data[f"{field_name}_download_url"] = (
                    download_url  # Guarda el enlace en updated_data
                )
                flash("Archivo subido exitosamente.", "success")
                return True
            else:
                flash(
                    "Error: El cliente de almacenamiento no está disponible.", "error"
                )
                return False
        except Exception as e:
            flash(f"Error al cargar el archivo: {str(e)}", "error")
            return False


def check_file_type(file):
    """Verifica que el tipo MIME del archivo sea permitido"""
    mime_type, _ = mimetypes.guess_type(file.filename)
    return mime_type in ALLOWED_MIME_TYPES


def delete_file(file_path):
    """Elimina un archivo del servidor"""
    client = current_app.storage.client
    if client is not None:
        try:
            client.remove_object(BUCKET_NAME, file_path)
            flash("Archivo eliminado exitosamente.", "success")
            return True
        except Exception as ex:
            flash(f"Error al eliminar el archivo: {ex}", "error")
            return False
    else:
        flash("Error: El cliente de almacenamiento no está disponible.", "error")
        return False
