
from flask import Flask
from config import config



def Create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    

    from api.views import views_blueprint
    # from api.views.views import views_blueprint
    app.register_blueprint(views_blueprint, url_prefix = '/api/v1')

    return app



# from api.views.create_redflag import create_redflag_blueprint
# from api.views.fetch_redflags import fetch_redflags_blueprint


# app.register_blueprint(create_redflag_blueprint, url_prefix ='/api/v1')
# app.register_blueprint(fetch_redflags_blueprint, url_prefix ='/api/v1')

