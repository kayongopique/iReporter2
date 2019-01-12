from flask import Blueprint
views_blueprint = Blueprint('views' , __name__)
from . import create_redflag , fetch_redflags, edit_redflag , delete_redflag,auth,admin