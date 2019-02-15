class Config:

    def init_app(app):
        pass

class DevConfig(Config):
    Debug = True
    CSRF_ENABLED = True
    MAIL_SERVER ='smtp.googleemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME ='kayongopique'
    MAIL_PASSWORD = 'bukirwa1994'
    MAIL_USE_TLS =True
    EMAIL_SUBJECT_PREFIX = '[Ireport]'
    MAIL_SENDER = 'kayongopique@gmail.com'
    ADMIN_EMAIL = 'kayongopique@gmail.com'
    DATABASE_URL = 'postgres://postgres:david@localhost:5432/ireporterdb'
    SECRET_KEY = 'rghhyfccxfbjgfdcvbjjhfdcvbn'

class TestingConfig(Config):
    testing = True  

class ProductionConfig(Config):
    debug =False

config = {
    'development': DevConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevConfig
}                   