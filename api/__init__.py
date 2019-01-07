
from flask import Flask

app = Flask(__name__)


# from api.views.create_redflag import create_redflag_blueprint
# from api.views.fetch_redflags import fetch_redflags_blueprint
from api.views.views import views_blueprint

# app.register_blueprint(create_redflag_blueprint, url_prefix ='/api/v1')
# app.register_blueprint(fetch_redflags_blueprint, url_prefix ='/api/v1')

app.register_blueprint(views_blueprint, url_prefix = '/api/v1')