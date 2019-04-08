from api import Create_app
from flask import Blueprint, render_template

template_blueprint = Blueprint('templates',__name__)

@template_blueprint.route('/')
def index():
    return render_template('index.html')




