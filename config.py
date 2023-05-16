import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qwertyuiopasdfghjkl'
    SQLAlchemy_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.environ.get("db_user")}:{os.environ.get("db_pwd")}@localhost/{os.environ.get("db_name")}'

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= os.environ.get('TEST_DB') or 'sqlite://'

config = {
    'dev': DevConfig,
    'testing': TestConfig,
    'default': DevConfig,
}