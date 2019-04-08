import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CSRF_ENABLED = True
    MAIL_SERVER ='smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('PASSWORD')
    MAIL_USE_TLS =True
    EMAIL_SUBJECT_PREFIX = '[Ireport]'

    def init_app(app):
        pass

class DevConfig(Config):
    Debug = True
    MAIL_SENDER = 'kayongopique@gmail.com'
    ADMIN_EMAIL = os.environ.get('ADMIN_MAIL')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    MAIL_SUBJECT_PREFIX = 'ireport'

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