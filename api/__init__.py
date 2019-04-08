
from flask import Flask
from flask_cors import CORS
from config import config
from flask_mail import Mail
cors = CORS()
mail = Mail()

def Create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    from api.views import views_blueprint
    from api.app import template_blueprint
    # from api.views.views import views_blueprint
    app.register_blueprint(views_blueprint, url_prefix = '/api/v1')
    app.register_blueprint(template_blueprint)
    return app



# from api.views.create_redflag import create_redflag_blueprint
# from api.views.fetch_redflags import fetch_redflags_blueprint


# app.register_blueprint(create_redflag_blueprint, url_prefix ='/api/v1')
# app.register_blueprint(fetch_redflags_blueprint, url_prefix ='/api/v1')

