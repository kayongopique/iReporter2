class Config:

    def init_app(app):
        pass

class DevConfig(Config):
    Debug = True
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