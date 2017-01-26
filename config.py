import os

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'secret key'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEV') or \
                              'postgresql://localhost/bucketlist_dev'


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user@localhost/bucketlist_test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_TEST') or \
                              'postgresql://localhost/bucketlist_test'
    SECRET_KEY = 'test secret key'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_PROD') or \
                              'postgresql://localhost/bucketlist_prod'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

