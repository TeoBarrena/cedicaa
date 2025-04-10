from flask import request, flash
import re
from src.core.jinete_amazonas import create_new_school, create_new_relative, get_rider_by_dni
from datetime import datetime
from src.core.jinete_amazonas.jinete_amazonas import Town

def validate_email(email):
    """Verifica si el email tiene un formato válido según una expresión regular."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def validate_school_grade(school_grade):
    """Valida que el grado escolar sea un número entre 1 y 6."""
    error = None
    try:
        school_grade = int(school_grade)  # Convertimos a entero
        if school_grade < 0 or school_grade >= 6:
            error = 'El grado debe ser un número mayor a 0 y menor a 6.'
    except ValueError:
        error = 'El grado debe ser un número entre 1 y 6.'
    return error

def validate_dni(dni):
    """Valida que el DNI no esté registrado y sea un número válido."""
    error = None
    if (get_rider_by_dni(dni)):
        error = 'Ya hay un Jinete o Amazona registrado con ese DNI.'
    else:
        try:
            dni = int(dni)
            if dni <= 0:
                error = 'El DNI debe ser un número mayor a 0.'
        except ValueError:
            error = 'El DNI debe ser un número válido.'
    return error


def create_school():
    """Crea una nueva institución escolar con los datos proporcionados en el formulario."""
    school_name = request.form.get('school_name')
    school_address = request.form.get('school_address')
    school_phone = request.form.get('school_phone')
    school_grade = request.form.get('school_grade')
    school_notes = request.form.get('school_notes')

    error = None
    if not school_name or not school_address or not school_phone or not school_grade:
        error = "Los campos Nombre, Dirección, Teléfono y Grado/Año de la escuela son obligatorios."
    else:
        error = validate_school_grade(school_grade)
    if error:
        return None, error
    
    # Crear una nueva institución escolar
    school = create_new_school(
        name=school_name,
        address=school_address,
        phone=school_phone,
        current_grade=school_grade,
        notes=school_notes
    )

    return school, None

def create_relative():
    """Crea uno o dos familiares asociados con los datos proporcionados en el formulario."""
    # Obtener los datos del primer familiar
    relationship = request.form.get('relative1_relationship')
    first_name = request.form.get('relative1_first_name')
    last_name = request.form.get('relative1_last_name')
    dni = request.form.get('relative1_dni')
    address = request.form.get('relative1_address')
    mobile = request.form.get('relative1_mobile')
    email = request.form.get('relative1_email')
    education = request.form.get('relative1_education')
    occupation = request.form.get('relative1_occupation')

    # Validaciones básicas del primer familiar
    error = None
    if not first_name or not last_name or not dni:
        error = 'Nombre, Apellido y DNI del familiar 1 son obligatorios.'
    else:
        error = validate_dni(dni)
        
    if not error and email and not validate_email(email):
        error = 'El formato del correo electrónico es inválido.'

    if error:
        return None, None, error

    # Crear la instancia del primer familiar (Relative)
    relative1 = create_new_relative(
        relationship=relationship,
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        address=address,
        mobile=mobile,
        email=email,
        education=education,
        occupation=occupation
    )

    relative2 = None 
    # Verificar si se desea agregar un segundo familiar
    if request.form.get('show_second_relative') == 'on':
        # Obtener los datos del segundo familiar
        relationship2 = request.form.get('relative2_relationship')
        first_name2 = request.form.get('relative2_first_name')
        last_name2 = request.form.get('relative2_last_name')
        dni2 = request.form.get('relative2_dni')
        address2 = request.form.get('relative2_address')
        mobile2 = request.form.get('relative2_mobile')
        email2 = request.form.get('relative2_email')
        education2 = request.form.get('relative2_education')
        occupation2 = request.form.get('relative2_occupation')

        error = validate_dni(dni2)

        # Validación del formato de email
        if not error and email2 and not validate_email(email2):
            error = 'El formato del correo electrónico del segundo familiar es inválido.'

        # Validaciones básicas del segundo familiar (opcional)
        if not error and first_name2 and last_name2 and dni2:
            # Crear la instancia del segundo familiar (Relative)
            relative2 = create_new_relative(
                relationship=relationship2,
                first_name=first_name2,
                last_name=last_name2,
                dni=dni2,
                address=address2,
                mobile=mobile2,
                email=email2,
                education=education2,
                occupation=occupation2
            )

    return relative1, relative2, error

def calculate_age(birth_date_str):
    """Calcula la edad en función de la fecha de nacimiento."""
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
    today = datetime.today().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def validate_birth_date(birth_date):
    """Valida una fecha de nacimiento y calcula la edad."""
    error = None
    age = 0

    if birth_date:
        try:
            age = calculate_age(birth_date)
            if age < 0:
                error = 'La fecha de nacimiento no puede ser en el futuro.'
            elif age > 120:
                error = 'La edad no es válida, no puede ser mayor a 120 años.'
        except ValueError:
            error = 'La fecha de nacimiento no es válida.'
    elif not error:
        error = 'La fecha de nacimiento es obligatoria.'

    return error, age


def validate_member_number(member_number):
    """Valida que el número de afiliado sea un número entero positivo."""
    error = None
    if member_number:
        try:
            member_number = int(member_number)
            if member_number < 0:
                error = 'El número de afiliado debe ser mayor a 0.'
        except ValueError:
            error = 'El número de afiliado no es válido.'
    elif not error:
        error = 'El número de afiliado es obligatorio.'

    return error
