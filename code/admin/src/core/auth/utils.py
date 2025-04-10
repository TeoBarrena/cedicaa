# Se llama con <td>{{ user.role.get_translated_name() }}</td>

ROLE_TRANSLATIONS = {
    "Technical": "Técnica",
    "Equestrian": "Ecuestre",
    "Volunteer": "Voluntariado",
    "Administration": "Administración",
    'Training': 'Capacitación', 
    "System Admin": "Administrador del sistema",
    "Editor": "Editor",
    "None": "Ninguno"
}

# Diccionario con todos los permisos
PERMISSIONS = [
    "user_index", "user_new", "user_destroy", "user_update", "user_show", "sa_user_show", "change_role", "change_active","change_password", "sa_user_update",
    "employee_index", "employee_create", "employee_destroy", "employee_update", "employee_show",
    "payments_index", "payments_create", "payments_destroy", "payments_update", "payments_show",
    "J&A_index", "J&A_create", "J&A_destroy", "J&A_update", "J&A_show",
    "collection_index", "collection_create", "collection_destroy", "collection_update", "collection_show",
    "equestrian_index", "equestrian_create", "equestrian_destroy", "equestrian_update", "equestrian_show",
    "contact_index", "contact_destroy", "contact_update", "contact_show", "contact_create", 
    "editor_index", "editor_create", "editor_destroy", "editor_update", "editor_show",
    "data_analysis_index", "data_analysis_show"
]

ROLE_PERMISSIONS = {
    "System Admin": [
        "user_index", "user_new", "user_destroy", "user_update", "user_show", "sa_user_show", "change_role", "change_active","change_password", "sa_user_update",
        "employee_index", "employee_create", "employee_destroy", "employee_update", "employee_show",
        "payments_index", "payments_create", "payments_destroy", "payments_update", "payments_show",
        "J&A_index", "J&A_create", "J&A_destroy", "J&A_update", "J&A_show",
        "collection_index", "collection_create", "collection_destroy", "collection_update", "collection_show",
        "equestrian_index", "equestrian_create", "equestrian_destroy", "equestrian_update", "equestrian_show",
        "contact_index", "contact_destroy", "contact_update", "contact_show",
        "editor_index", "editor_create", "editor_destroy", "editor_update", "editor_show",
        "data_analysis_index", "data_analysis_show"
    ],
    "Administration": [
        "user_show", "user_update",
        "employee_index", "employee_create", "employee_destroy", "employee_update", "employee_show",
        "payments_index", "payments_create", "payments_destroy", "payments_update", "payments_show",
        "J&A_index", "J&A_create", "J&A_destroy", "J&A_update", "J&A_show",
        "collection_index", "collection_create", "collection_destroy", "collection_update", "collection_show",
        "equestrian_index", "equestrian_show",
        "contact_index", "contact_destroy", "contact_update", "contact_show",
        "data_analysis_index", "data_analysis_show",
        "editor_index", "editor_create", "editor_destroy", "editor_update", "editor_show"
    ],
    "Technical": [
        "user_show", "user_update",
        "J&A_index", "J&A_create", "J&A_destroy", "J&A_update", "J&A_show",
        "collection_index", "collection_show",
        "equestrian_index", "equestrian_show",
        "data_analysis_index", "data_analysis_show"
    ],
    "Equestrian": [
        "user_show", "user_update",
        "J&A_index", "J&A_show", "equestrian_index", "equestrian_create", "equestrian_show"
    ],
    "Editor": [
        "user_show", "user_update",
        "editor_index", "editor_create", "editor_update", "editor_show"
    ],
    "Volunteer": [
        "user_show", "user_update"
    ],
    "Training": [
        "user_show", "user_update"
    ],
    "None": [
        "user_show", "user_update"
    ]
}