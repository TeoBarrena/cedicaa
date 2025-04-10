from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from src.core.jinete_amazonas.utils import DIAGNOSIS, DISABILITY_TYPE, FAMILY_ALLOWANCE, PROPOSAL_TYPES, CONDITIONS, LOCATIONS, DAYS, EDUCATION_LEVEL, PROVINCE_TOWNS
from src.core.jinete_amazonas import create_new_rider, show_list_riders, update_rider_bd, delete_rider, get_institution_employees, get_rider_by_id, get_towns_by_province, create_new_document, get_not_deleted_documents, get_document_by_id, delete_document
from src.web.controllers.jinete_amazonas.jinete_amazonas_functions_without_url import create_school, create_relative, validate_dni, validate_birth_date,  validate_member_number, validate_school_grade, validate_email
from src.web.handlers.auth import check
from src.web.handlers.files import handle_file_upload
from src.core.employees import save_files
from datetime import datetime

bp = Blueprint("jinete_amazonas", __name__, url_prefix="/jinete_amazonas")


@bp.route("/list_riders", methods=['GET'])
@check("J&A_index")
def list_riders():
    """Muestra una lista paginada de jinetes y amazonas, con opciones de búsqueda, ordenamiento, y paginación."""
    
    # Obtener parámetros de búsqueda
    search_query = request.args.get('search', '')
    order_by = request.args.get('order_by', 'first_name')
    order_dir = request.args.get('order_dir', 'asc')
    per_page = request.args.get('per_page', 5, type=int)
    page = request.args.get('page', 1, type=int)

    riders_pagination = show_list_riders(search_query,order_by, order_dir, page, per_page)

    return render_template('jinete_amazonas/index.html', 
                            riders_pagination=riders_pagination, 
                            search_query=search_query, 
                            order_by=order_by, 
                            order_dir=order_dir, 
                            per_page=per_page)



@bp.route("/create_rider", methods=['GET', 'POST'])
@check("J&A_create")
def create_rider():
    """Maneja la creación de un nuevo jinete o amazona. Si el método es POST, valida los datos del formulario, los guarda y redirige a la lista de jinetes. 
    Si el método es GET, muestra el formulario de creación."""
    today = datetime.now().date()
    error = None
    if request.method == 'POST':
        #DATOS PERSONALES DEL JINETE O AMAZONA:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dni = request.form.get('dni')
        if not first_name or not last_name or not dni:
            error = "El nombre, apellido y DNI son obligatorios."
        if not error and dni:
            error = validate_dni(dni) 
        age = 0
        if not error:   
            birth_date = request.form.get('birth_date')
            error, age = validate_birth_date(birth_date)
        if not error:
            member_number = request.form.get('member_number')
            error = validate_member_number(member_number)
        
        if not error:
            school, error = create_school()
        if not error:
            relative1, relative2, error= create_relative()
        if not error:
            town_id = int(request.form.get("town_id"))
            town_id_of_birth = int(request.form.get("town_id_of_birth"))
            phone = request.form.get('phone')
            emergency_contact = request.form.get('emergency_contact')
            emergency_phone = request.form.get('emergency_phone')
            scholarship = request.form.get('scholarship') == 'yes'
            scholarship_notes = request.form.get('scholarship_notes')
            has_disability_certificate = request.form.get('has_disability_certificate') == 'yes'
            diagnosis = request.form.get('diagnosis')
            other_diagnosis = request.form.get('other_diagnosis')
            disability_types = request.form.getlist('disability_type')
            family_allowance = request.form.get('family_allowance') == 'yes'
            allowance_type = request.form.getlist('allowance_type')
            pension = request.form.get('pension') == 'yes'
            pension_type = request.form.get('pension_type')

            address = request.form.get("address")
            number = int(request.form.get("number"))
            apartment = request.form.get("apartment")

            #SITUACIÓN PREVISIONAL
            social_security = request.form.get('social_security')
            cure = request.form.get('cure') == 'yes'
            social_security_notes = request.form.get('social_security_notes')


            #PROFESIONALES que lo ATIENDEN:
            professionals = request.form.get('professionals')

            #TRABAJO EN NUESTRA INSTITUCIÓN:
            proposal_type = request.form.get('proposal_type')
            condition = request.form.get('condition')
            location = request.form.get('location')
            days = request.form.getlist('days[]')
            days = ', '.join(days)
            therapist = request.form.get('therapist')
            driver = request.form.get('driver')
            horse = request.form.get('horse')
            assistant = request.form.get('assistant')

            rider = create_new_rider(
                #DATOS PERSONALES DEL JINETE O AMAZONA:
                first_name=first_name,
                last_name=last_name,
                dni=dni,
                age=age,
                birth_date=birth_date,
                town_id=town_id,
                town_id_of_birth = town_id_of_birth,
                address = address,
                number = number,
                apartment = apartment,
                phone=phone if phone else None,
                emergency_contact=emergency_contact if emergency_contact else None,
                emergency_phone=emergency_phone if emergency_phone else None,
                scholarship=scholarship,
                scholarship_notes=scholarship_notes if scholarship_notes else None,
                has_disability_certificate=has_disability_certificate,
                diagnosis=diagnosis,
                other_diagnosis=other_diagnosis if other_diagnosis else None,
                disability_type=", ".join(disability_types) if disability_types else None,
                family_allowance=family_allowance,
                allowance_type=", ".join(allowance_type) if allowance_type else None,
                pension=pension,
                pension_type=pension_type if pension_type else None,

                #SITUACIÓN PREVISIONAL
                social_security=social_security if social_security else None,
                member_number=member_number if member_number else None,
                cure=cure,
                social_security_notes=social_security_notes if social_security_notes else None,

                #INSTITUCIÓN ESCOLAR a la que CONCURRE ACTUALMENTE:
                school_id=school.id,

                #PROFESIONALES que lo ATIENDEN:
                professionals=professionals if professionals else None,

                #DATOS PERSONALES De FAMILIAR/es O TUTOR/es RESPONSABLE/s:
                relative_id1 = relative1.id,
                relative_id2 = relative2.id if relative2 else None,

                #TRABAJO EN NUESTRA INSTITUCIÓN:
                proposal_type = proposal_type,
                condition = condition,
                location = location,
                days = days,
                therapist_id = therapist,
                driver_id = driver,
                horse_id = horse,
                assistant_id = assistant,
            )

            flash(f"Jinete o Amazona {rider.first_name} creado exitosamente.", "success")

            
            return redirect(url_for('jinete_amazonas.list_riders'))
        

    therapists, horses, drivers, assistants = get_institution_employees()

    return render_template('jinete_amazonas/create.html',  
        provinces=PROVINCE_TOWNS,
        diagnosis_options=DIAGNOSIS, 
        disability_types=DISABILITY_TYPE, 
        family_allowance=FAMILY_ALLOWANCE,
        proposal_types=PROPOSAL_TYPES,
        conditions=CONDITIONS,
        locations=LOCATIONS,
        days_options=DAYS,
        education_options=EDUCATION_LEVEL,
        therapists=therapists,
        drivers=drivers,
        horses=horses,
        assistants=assistants,
        error=error,
        form=request.form,
        today=today)


@bp.route("/get_towns_by_province/<int:province_id>")
@check("employee_index")
def get_towns_by_province(province_id):
    """Devuelve las localidades correspondientes a una provincia en formato JSON."""
    # Obtener las localidades correspondientes a la provincia seleccionada
    towns = get_towns_by_province(province_id)
    
    # Verifica que las localidades se están obteniendo correctamente
    if not towns:
        return jsonify({'error': 'No towns found'}), 404

    # Devolver los datos en formato JSON
    return jsonify({'towns': [{'id': town.id, 'name': town.name} for town in towns]})



@bp.route('/rider_show/<int:rider_id>', methods=['GET'])
@check("J&A_show")
def view_rider(rider_id):
    """Muestra los detalles de un jinete o amazona seleccionado. Solo permite ver, sin edición."""
    rider = get_rider_by_id(rider_id)
    
    if not rider:
        flash('No se pudo obtener el ID del jinete o amazona.', 'danger')
        return redirect(url_for('jinete_amazonas.list_riders'))


    therapists, horses, drivers, assistants = get_institution_employees()

    return render_template('jinete_amazonas/show.html', 
        rider=rider, 
        provinces=PROVINCE_TOWNS,
        diagnosis_options=DIAGNOSIS, 
        disability_types=DISABILITY_TYPE, 
        family_allowance=FAMILY_ALLOWANCE,
        proposal_types=PROPOSAL_TYPES,
        conditions=CONDITIONS,
        locations=LOCATIONS,
        days_options=DAYS,
        education_options=EDUCATION_LEVEL,
        therapists=therapists,
        drivers=drivers,
        horses=horses,
        assistants=assistants)


@bp.route('/update_rider/<int:rider_id>', methods=['GET', 'POST'])
@check("J&A_update")
def update_rider(rider_id):
    """Muestra y permite editar los detalles de un jinete o amazona seleccionado. Actualiza la información si el método es POST, validando los datos y mostrando mensajes flash en caso de error."""
    today = datetime.now().date()
    rider = get_rider_by_id(rider_id)

    if not rider:
        flash('No se pudo obtener el jinete o amazona.', 'danger')
        return redirect(url_for('jinete_amazonas.list_riders'))
    
    errors = []
    if request.method == 'POST':
        # Actualizar los datos del jinete con los valores del formulario
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if first_name != rider.first_name:
            rider.first_name = first_name
        if last_name != rider.last_name:
            rider.last_name = last_name

        dni = request.form.get('dni')
        if dni != rider.dni:
            error = validate_dni(dni)
            if error:
                flash(error, 'danger')
            else:
                rider.dni = dni

        
        birth_date = request.form.get('birth_date')
        if birth_date != str(rider.birth_date):
            error, age = validate_birth_date(birth_date)
            if error:
                flash(error, 'danger')
                return redirect(url_for('jinete_amazonas.update_rider', rider_id=rider.id))      
            else:
                rider.birth_date= birth_date
                rider.age = age
        
        rider.address = request.form.get('address')
        rider.number = request.form.get('number')
        rider.town_id = request.form.get('town_id')

        apartment_db_value = rider.apartment if rider.apartment is not None else ""
        if request.form.get('apartment') != apartment_db_value:
            rider.apartment = request.form.get('apartment')

        school_name = request.form.get('school_name')
        school_address = request.form.get('school_address')
        school_phone = request.form.get('school_phone')
        school_grade = request.form.get('school_grade')
        
        rider.school.name = school_name
        rider.school.address = school_address
        rider.school.phone = school_phone
        error = validate_school_grade(school_grade)
        if error:
            flash(error, 'danger')
            return redirect(url_for('jinete_amazonas.update_rider', rider_id=rider.id))   
        else:
            rider.school.current_grade = school_grade
        
        school_notes_db_value = rider.school.notes if rider.school.notes is not None else ""
        if request.form.get('school_notes') != school_notes_db_value:
            rider.school.notes = request.form.get('school_notes')

        
        rider.relative1.first_name = request.form.get('relative1_first_name')
        rider.relative1.last_name = request.form.get('relative1_last_name')
        relative1_dni = request.form.get('relative1_dni')

        if relative1_dni != rider.relative1.dni:
            error = validate_dni(relative1_dni)
            if error:
                flash(error, 'danger')
            else:
                rider.relative1.dni = relative1_dni

        
        relative2_dni = request.form.get('relative2_dni')
        if relative2_dni:
            if relative2_dni != rider.relative2.dni:
                error = validate_dni(relative2_dni)
                if error:
                    flash(error, 'danger')
                else:
                    rider.relative2.dni = relative2_dni


        relative1_email = request.form.get('relative1_email')
        if relative1_email and not validate_email(relative1_email):
            flash('El formato del correo electrónico del familiar 1 es inválido.', 'danger')
            return redirect(url_for('jinete_amazonas.update_rider', rider_id=rider.id))   
        else:
            rider.relative1.email = relative1_email


        relative2_email = request.form.get('relative2_email')
        if relative2_email:
            if not validate_email(relative2_email):
                flash('El formato del correo electrónico del familiar 2 es inválido.', 'danger')
                return redirect(url_for('jinete_amazonas.update_rider', rider_id=rider.id))
            else:
                rider.relative2.email = relative2_email


        town_id_form_value = request.form.get('town_id')
        if town_id_form_value is not None and town_id_form_value.isdigit():
            town_id_form_value = int(town_id_form_value)
            if town_id_form_value != rider.town_id:
                rider.town_id = town_id_form_value
        

        town_id_of_birth = request.form.get("town_id_of_birth")
        if town_id_of_birth != rider.town_id_of_birth:
            rider.town_id_of_birth = town_id_of_birth
    
        phone_db_value = rider.phone if rider.phone is not None else ""
        if request.form.get('phone') != phone_db_value:
            rider.phone = request.form.get('phone')

        emergency_contact_db_value = rider.emergency_contact if rider.emergency_contact is not None else ""
        if request.form.get('emergency_contact') != emergency_contact_db_value :
            rider.emergency_contact = request.form.get('emergency_contact')

        emergency_phone_db_value = rider.emergency_phone if rider.emergency_phone is not None else ""
        if request.form.get('emergency_phone') != emergency_phone_db_value:
            rider.emergency_phone = request.form.get('emergency_phone')

        if request.form.get('scholarship') == 'True' and not rider.scholarship:
            rider.scholarship = True
        elif request.form.get('scholarship') == 'False' and rider.scholarship:
            rider.scholarship = False

        scholarship_notes_db_value = rider.scholarship_notes if rider.scholarship_notes is not None else "" 
        if request.form.get('scholarship_notes') != scholarship_notes_db_value:
            rider.scholarship_notes = request.form.get('scholarship_notes')

        if request.form.get('has_disability_certificate') == 'True' and not rider.has_disability_certificate:
            rider.has_disability_certificate = True

        elif request.form.get('has_disability_certificate') == 'False' and rider.has_disability_certificate:
            rider.has_disability_certificate = False

        diagnosis_db_value = rider.diagnosis if rider.diagnosis is not None else ""
        if request.form.get('diagnosis') != diagnosis_db_value:
            rider.diagnosis = request.form.get('diagnosis')

        other_diagnosis_form_value = request.form.get('other_diagnosis')
        other_diagnosis_form_value = other_diagnosis_form_value if other_diagnosis_form_value else ""
        other_diagnosis_db_value = rider.other_diagnosis if rider.other_diagnosis else ""

        if other_diagnosis_form_value != other_diagnosis_db_value:
            rider.other_diagnosis = other_diagnosis_form_value


        disability_type_list = sorted(request.form.getlist('disability_type'))
        rider_disability_type_list = sorted(rider.disability_type.split(', ')) if rider.disability_type else []
        if disability_type_list != rider_disability_type_list:
            rider.disability_type = ', '.join(disability_type_list)

        if request.form.get('family_allowance') == 'True' and not rider.family_allowance:
            rider.family_allowance = True
        elif request.form.get('family_allowance') == 'False' and rider.family_allowance:
            rider.family_allowance = False

        allowance_type_list = sorted(request.form.getlist('allowance_type'))
        rider_allowance_type_list = sorted(rider.allowance_type.split(', ')) if rider.allowance_type else []
        if allowance_type_list != rider_allowance_type_list:
            rider.allowance_type = ', '.join(allowance_type_list)
        
        if request.form.get('pension') == 'True' and not rider.pension:
            rider.pension = True
        elif request.form.get('pension') == 'False' and rider.pension:
            rider.pension = False

        
        if request.form.get('pension_type') != rider.pension_type:
            rider.pension_type = request.form.get('pension_type')

        social_security_db_value = rider.social_security if rider.social_security is not None else "" 
        if request.form.get('social_security') != social_security_db_value:
            rider.social_security = request.form.get('social_security')
        
        member_number_db_value = rider.member_number if rider.member_number is not None else "" 
        if request.form.get('member_number') != member_number_db_value:
            rider.member_number = request.form.get('member_number')
        
        if request.form.get('cure') == 'True' and not rider.cure:
            rider.cure = True
        elif request.form.get('cure') == 'False' and rider.cure:
            rider.cure = False

        social_security_notes_db_value = rider.social_security_notes if rider.social_security_notes is not None else "" 
        if request.form.get('social_security_notes') != social_security_notes_db_value:
            rider.social_security_notes = request.form.get('social_security_notes')

        
        professionals_db_value = rider.professionals if rider.professionals is not None else "" 
        if request.form.get('professionals') != professionals_db_value:
            rider.professionals = request.form.get('professionals')

        # Actualizar datos de familiares
        if request.form.get('relative1_relationship') != rider.relative1.relationship:
            rider.relative1.relationship = request.form.get('relative1_relationship')

        if request.form.get('relative1_first_name') != rider.relative1.first_name:
            rider.relative1.first_name = request.form.get('relative1_first_name')

        if request.form.get('relative1_last_name') != rider.relative1.last_name:
            rider.relative1.last_name = request.form.get('relative1_last_name')

        
        if request.form.get('relative1_address') != rider.relative1.address:
            rider.relative1.address = request.form.get('relative1_address')

        if request.form.get('relative1_mobile') != rider.relative1.mobile:
            rider.relative1.mobile = request.form.get('relative1_mobile')

        
        if request.form.get('relative1_education') != rider.relative1.education:
            rider.relative1.education = request.form.get('relative1_education')

        if request.form.get('relative1_occupation') != rider.relative1.occupation:
            rider.relative1.occupation = request.form.get('relative1_occupation')

        if request.form.get('show_second_relative'):
            if request.form.get('relative2_relationship') != rider.relative2.relationship:
                rider.relative2.relationship = request.form.get('relative2_relationship')

            if request.form.get('relative2_first_name') != rider.relative2.first_name:
                rider.relative2.first_name = request.form.get('relative2_first_name')

            if request.form.get('relative2_last_name') != rider.relative2.last_name:
                rider.relative2.last_name = request.form.get('relative2_last_name')

            if request.form.get('relative2_dni') != rider.relative2.dni:
                rider.relative2.dni = request.form.get('relative2_dni')

            if request.form.get('relative2_address') != rider.relative2.address:
                rider.relative2.address = request.form.get('relative2_address')

            if request.form.get('relative2_mobile') != rider.relative2.mobile:
                rider.relative2.mobile = request.form.get('relative2_mobile')

            if request.form.get('relative2_education') != rider.relative2.education:
                rider.relative2.education = request.form.get('relative2_education')

            if request.form.get('relative2_occupation') != rider.relative2.occupation:
                rider.relative2.occupation = request.form.get('relative2_occupation')

        # Propuesta de trabajo institucional
        if request.form.get('proposal_type') != rider.proposal_type:
            rider.proposal_type = request.form.get('proposal_type')

        if request.form.get('condition') != rider.condition:
            rider.condition = request.form.get('condition')

        if request.form.get('location') != rider.location:
            rider.location = request.form.get('location')


        days_list = request.form.getlist('days[]')
        if not days_list:
            flash('Debes seleccionar al menos un día.', 'danger')
            return redirect(url_for('jinete_amazonas.update_rider', rider_id=rider.id))
        else:
            rider_days_list = rider.days.split(', ') if rider.days else []
            if sorted(days_list) != sorted(rider_days_list):
                rider.days = ', '.join(days_list)


        # Actualizar IDs de relaciones
        therapist_form_value = request.form.get('therapist')
        if therapist_form_value is not None and therapist_form_value.isdigit():
            therapist_form_value = int(therapist_form_value)
            if therapist_form_value != rider.therapist.id:
                rider.therapist_id = therapist_form_value

        driver_form_value = request.form.get('driver')
        if driver_form_value is not None and driver_form_value.isdigit():
            driver_form_value = int(driver_form_value)
            if driver_form_value != rider.driver.id:
                rider.driver_id = driver_form_value

        horse_form_value = request.form.get('horse')
        if horse_form_value is not None and horse_form_value.isdigit():
            horse_form_value = int(horse_form_value)
            if horse_form_value != rider.horse.id:
                rider.horse_id = horse_form_value

        assistant_form_value = request.form.get('assistant')
        if assistant_form_value is not None and assistant_form_value.isdigit():
            assistant_form_value = int(assistant_form_value)
            if assistant_form_value != rider.assistant.id:
                rider.assistant_id = assistant_form_value

        try:
            update_rider_bd()
            flash('Los datos del Jinete o Amozona han sido actualizados exitosamente.', 'success')
        except ValueError as ve:
            flash(str(ve), "warning")
        except Exception as e:
            flash(f"Error al actualizar el Jinete o Amazona: {str(e)}", "error")

    therapists, horses, drivers, assistants = get_institution_employees()

    return render_template('jinete_amazonas/update.html', 
        rider=rider, 
        provinces=PROVINCE_TOWNS,
        diagnosis_options=DIAGNOSIS, 
        disability_types=DISABILITY_TYPE, 
        family_allowance=FAMILY_ALLOWANCE,
        proposal_types=PROPOSAL_TYPES,
        conditions=CONDITIONS,
        locations=LOCATIONS,
        days_options=DAYS,
        education_options=EDUCATION_LEVEL,
        therapists=therapists,
        drivers=drivers,
        horses=horses,
        assistants=assistants,
        today = today)
        


@bp.route('/destroy_rider/<int:rider_id>', methods=['POST'])
@check("J&A_destroy")
def destroy_rider(rider_id):
    """Elimina un jinete o amazona del sistema."""
    try:
        rider = delete_rider(rider_id)
        flash(f"El jinete {rider.dni} ha sido eliminado exitosamente.", "success")
        return redirect(url_for('jinete_amazonas.list_riders'))
    except ValueError as ve:
        flash(str(ve), "error")
        return redirect(url_for('jinete_amazonas.list_riders'))
    except Exception as e:
        flash(f"Error al eliminar el rider: {str(e)}", "error")
        return redirect(url_for('jinete_amazonas.list_riders'))


@bp.route('/upload_document/<int:rider_id>', methods=['POST'])
@check("J&A_update")
def upload_document(rider_id):
    """Carga un documento de un rider especifico al sistema."""
    rider = get_rider_by_id(rider_id)
    
    # Extraer datos del formulario
    new_data = request.form.copy()
    new_data["title"] = request.form.get('title')
    new_data["document_type"] = request.form.get('document_type')
    new_data["file_url"] = request.form.get('file_url')
    new_data["is_external"] = bool(new_data["file_url"])  # Verificar si es un enlace externo
    new_data["file"] = None  # Inicializar como None si no se sube un archivo
    
    try:
        # Si el documento es un enlace externo
        if new_data["is_external"]:
            document = create_new_document(
                rider_id=rider.id,
                title=new_data["title"],
                document_type=new_data["document_type"],
                file_path=new_data["file_url"],
                is_external=True
            )
        else:
            # Verificar si se subió un archivo
            file = request.files.get('file')
            if file and file.filename:  # Verificar que haya un archivo y tenga nombre
                document = handle_file_upload('file', new_data, 'rider', rider)
                if (document == False):
                    raise Exception
                else: 
                    create_new_document(
                        rider_id=rider.id,
                        title=new_data["title"],
                        document_type=new_data["document_type"],
                        file_path=new_data.get('file'),
                        is_external=False
                    )
            else:
                flash("Debes subir un archivo o proporcionar un enlace.", "error")
                return redirect(url_for('jinete_amazonas.view_documents', rider_id=rider.id))
        
        # Guardar los cambios y mostrar éxito
        save_files()
        #flash("Documento cargado correctamente.", "success")
        return redirect(url_for('jinete_amazonas.view_documents', rider_id=rider.id))
    
    except Exception as e:
        #flash(f"Error al cargar el documento: {str(e)}", "error")
        return redirect(url_for('jinete_amazonas.view_documents', rider_id=rider.id))


@bp.route('/rider/<int:rider_id>/documents', methods=['GET'])
@check("J&A_index")
def view_documents(rider_id):
    """Muestra una lista paginada de documentos, con opciones de búsqueda, ordenamiento, y paginación."""
    rider = get_rider_by_id(rider_id)
    
    # Parámetros de búsqueda y ordenación
    search_title = request.args.get('search_title', '').strip()
    document_type = request.args.get('document_type', '')
    sort_by = request.args.get('sort_by', 'uploaded_at')
    order = request.args.get('order', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de documentos por página
    
    # Obtener documentos no eliminados con búsqueda y ordenación
    documents = get_not_deleted_documents(rider_id, page, per_page, search_title, document_type, sort_by, order)
    
    return render_template('jinete_amazonas/index_file.html', rider=rider, documents=documents, search_title=search_title, document_type=document_type, sort_by=sort_by, order=order)

@bp.route('/document/<int:document_id>/edit', methods=['GET', 'POST'])
@check("J&A_update")
def update_document(document_id):
    """Muestra y permite editar los detalles de un documento seleccionado. Actualiza la información si el método es POST, validando los datos y mostrando mensajes flash en caso de error."""
    document = get_document_by_id(document_id)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        title = request.form.get('title')
        document_type = request.form.get('document_type')
        file_url = request.form.get('file_url')

        # Actualizar los campos del documento
        document.title = title
        document.document_type = document_type

        if file_url:
            document.file_path = file_url
            document.is_external = True
        else:
            file = request.files.get('file')
            updated_data = request.form.copy()
            if file and file.filename:
                updated_data = {}
                handle_file_upload('file', updated_data, 'rider', document)
                if (updated_data != {}):
                    document.file_path = updated_data['file']
                    document.is_external = False

        save_files()
        flash("Documento actualizado correctamente.", "success")
        return redirect(url_for('jinete_amazonas.view_documents', rider_id=document.rider_id))

    return render_template('jinete_amazonas/update_file.html', document=document)
@bp.route('/document/<int:document_id>/delete', methods=['GET'])
@check("J&A_delete")
def destroy_document(document_id):
    """Elimina documento de un jinete o amazona del sistema."""
    document = delete_document(document_id)
    
    if document:
        flash('Documento eliminado correctamente.', 'success')
    else:
        flash('El documento no fue encontrado.', 'error')
    
    return redirect(url_for('jinete_amazonas.view_documents', rider_id=document.rider_id))
