from src.web.handlers.auth import is_authenticated, check_permission
from src.core.auth import is_system_admin, get_current_user
from src.core.equestrian.utils import get_rider_types, get_acquisition, get_horse_gender
from src.core.equestrian import get_associated_employees
from src.core.employees import get_active_trainers
from src.web import helpers
from src.web.controllers.horses import delete_file

def register(app):
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(check_permission=check_permission)
    app.jinja_env.globals.update(is_system_admin=is_system_admin)
    app.jinja_env.globals.update(current_user=get_current_user)
    app.jinja_env.globals.update(get_rider_types=get_rider_types) 
    app.jinja_env.globals.update(get_acquisition=get_acquisition)  
    app.jinja_env.globals.update(get_horse_gender=get_horse_gender)
    app.jinja_env.globals.update(get_associated_employees=get_associated_employees)
    app.jinja_env.globals.update(get_active_trainers=get_active_trainers)
    app.jinja_env.globals.update(file_url=helpers.file_url)
    app.jinja_env.globals.update(delete_file=delete_file)
