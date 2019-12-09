import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    FILE_PATH = "/home/sameer/litmusblox-backend/FileStore/processed_files/"


class ProductionConfig(BaseConfig):
    FILE_PATH = ""
    FLASK_ENV = 'production'


class TestConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    FILE_PATH = "/home/lbtest/serverApplication/FileStore/processed_files/"
